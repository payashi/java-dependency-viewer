from concurrent.futures import ThreadPoolExecutor
import os
import re
import subprocess
from typing import Dict, Iterable, List, Set, Union


class Analyzer:
    def __init__(self):
        # 正規表現を事前にコンパイル
        self.this_class_pattern = re.compile(r"this_class:\s+#\d+\s+//\s+([\w/.$]+)")
        self.constant_pool_pattern = re.compile(
            r"#\d+\s+=\s+Class\s+#\d+\s+//\s+([\w/.$]+)"
        )

    def analyze_from_str(self, javap_output: str) -> Dict[str, Set[str]]:
        """
        javap の出力から、対象クラスと依存クラスを抽出します。
        """
        # ログをセクションごとに分割
        sections = javap_output.split("Constant pool:")
        if len(sections) < 2:
            raise ValueError(
                "Invalid javap output format. 'Constant pool' section not found."
            )

        # クラス名を取得
        this_class_match = self.this_class_pattern.search(sections[0])
        if not this_class_match:
            print("Invalid javap output format. 'this_class' not found.")
            return {}
        current_class = this_class_match.group(1).replace("/", ".")

        # Constant pool を解析して依存クラスを取得
        dependencies = set()
        constant_pool_section = sections[1]
        constant_pool_matches = self.constant_pool_pattern.findall(
            constant_pool_section
        )
        for match in constant_pool_matches:
            dependencies.add(match.replace("/", "."))
        dependencies.discard(current_class)

        return {current_class: dependencies}

    def analyze_from_class_dir(self, class_dir_path: str) -> Dict[str, Set[str]]:
        class_paths = []
        for root, _, files in os.walk(class_dir_path):
            for file in files:
                if file.endswith(".class"):
                    class_paths.append(os.path.join(root, file))
        source_file_all = self.run(class_paths)

        sections = self._split_sections(source_file_all)

        with ThreadPoolExecutor() as executor:
            results: List[Dict[str, Set[str]]] = list(
                executor.map(self.analyze_from_str, sections)
            )

        results = {key: value for result in results for key, value in result.items()}
        return results

    def _split_sections(self, source: str) -> Iterable[str]:
        classfile_pattern = re.compile(r"\nClassfile.*\n")
        sections = re.split(classfile_pattern, source)
        return sections

    def run(self, class_paths: Union[str, Iterable[str]]) -> str:
        if isinstance(class_paths, str):
            class_paths = [class_paths]
        try:
            # subprocess.run を使用して javap を実行
            result = subprocess.run(
                ["javap", "-verbose", *class_paths],  # javap コマンドと引数
                capture_output=True,  # 標準出力とエラー出力をキャプチャ
                text=True,  # 出力を文字列として取得
                check=True,  # エラー時に例外をスロー
            )
            return result.stdout  # 標準出力を返す
        except subprocess.CalledProcessError as e:
            print(f"Error running javap: {e.stderr}")
            raise


# 使用例
if __name__ == "__main__":
    class_dir_path = os.path.join(
        os.path.dirname(__file__), os.pardir, "tests", "data", "classes", "com"
    )
    try:
        analyzer = Analyzer()
        class_dependencies = analyzer.analyze_from_class_dir(class_dir_path)
        print(class_dependencies)
    except Exception as e:
        print(f"Failed to analyze class file: {e}")
