import re
from typing import Any
from typing import Optional

class LaTeXResumeParser:
    def parse(self, text: str) -> str:
        """
        Parse LaTeX content from various LLM output formats.
        Supports both ```latex and standard ``` code blocks.
        
        Args:
            text (str): The text containing LaTeX code blocks
            
        Returns:
            str: Extracted LaTeX content
            
        Raises:
            ValueError: If no valid LaTeX content is found
        """
        # print(text)
        # Try different patterns for matching LaTeX content
        patterns = [
            # Standard markdown LaTeX block
            r"```latex\s*(.*?)\s*```",
            # Generic code block that might contain LaTeX
            r"```\s*(\\documentclass.*?)\s*```",
            # Alternate format with latex keyword
            r"```\s*latex\s*(.*?)\s*```",
            # Basic code block containing LaTeX indicators
            r"```\s*(.*?\\begin\{document\}.*?)```"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                # Extract and clean the content
                content = match.group(1).strip()
                # Verify it looks like LaTeX
                if self._validate_latex_content(content):
                    return content
                
        raise ValueError("No valid LaTeX content found in the output.")
    
    def _validate_latex_content(self, content: str) -> bool:
        """
        Basic validation to ensure content appears to be LaTeX.
        
        Args:
            content (str): The extracted content to validate
            
        Returns:
            bool: True if content appears to be valid LaTeX
        """
        latex_indicators = [
            r"\\documentclass",
            r"\\begin\{document\}",
            r"\\end\{document\}",
            r"\\section",
            r"\\subsection",
            r"\\textbf",
            r"\\textit"
        ]
        
        # Check if at least one LaTeX indicator is present
        return any(re.search(indicator, content) for indicator in latex_indicators)
    
    @property
    def type(self) -> str:
        """Return the type identifier for the parser."""
        return "latex_document"