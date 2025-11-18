import coverage
import os
import logging
from typing import Dict, Union


class CoverageAnalyzer:
    def __init__(self, branch: bool = True):
        self.logger = logging.getLogger(__name__)
        self.cov = coverage.Coverage(branch=branch)

    def analyze_coverage(self, source_path: str, include_pattern: str = "*.py") -> Dict[str, Union[int, float]]:

        if not os.path.exists(source_path):
            raise ValueError(f"Error: Source path does not exist: {source_path}")

        try:
            self.cov = coverage.Coverage(
                source=[source_path],
                include=include_pattern,
                branch=True
            )

            self.logger.debug(f"Starting coverage analysis for {source_path}")
            self.cov.start()

            for root, _, files in os.walk(source_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            self.logger.debug(f"Processing file: {file_path}")
                            with open(file_path, 'r', encoding='utf-8') as f:
                                code = compile(f.read(), file_path, 'exec')
                                exec(code, {})
                        except Exception as e:
                            self.logger.warning(f"Error: Failed to process {file_path}: {str(e)}")
                            continue

            self.cov.stop()
            self.cov.save()

            total_statements = 0
            total_missing = 0
            files_analyzed = 0
            excluded_lines = 0

            measured_files = self.cov.get_data().measured_files()

            for filename in measured_files:
                try:
                    analysis = self.cov.analysis(filename)
                    statements = set(analysis[1])
                    missing = set(analysis[2])
                    excluded = set(analysis[3])

                    total_statements += len(statements)
                    total_missing += len(missing - excluded)
                    excluded_lines += len(excluded)
                    files_analyzed += 1
                except Exception as e:
                    self.logger.error(f"Analysis failed for {filename}: {str(e)}")

            coverage_percentage = 0.0
            if total_statements > 0:
                coverage_percentage = round(
                    ((total_statements - total_missing) / total_statements) * 100,
                    2
                )

            result = {
                'total_lines': total_statements,
                'missing_lines': total_missing,
                'excluded_lines': excluded_lines,
                'files_analyzed': files_analyzed,
                'coverage_percentage': coverage_percentage
            }

            self.logger.info(f"Coverage analysis completed: {result}")
            return result

        except Exception as e:
            self.logger.error(f"Coverage analysis failed: {str(e)}")
            raise Exception(f"Error: Coverage analysis failed: {str(e)}")

        finally:
            self.cov.erase()