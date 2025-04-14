import os
import logging
from docx import Document
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

logger = logging.getLogger(__name__)

def extract_cell_text(cell: _Cell) -> str:
    """Extract text from a table cell, including any paragraphs and nested tables"""
    text = []
    for paragraph in cell.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)
    for table in cell.tables:
        table_text = extract_table_text(table)
        if table_text.strip():
            text.append(table_text)
    return '\n'.join(text)

def extract_table_text(table: Table) -> str:
    """Extract text from a table, preserving structure"""
    rows = []
    for row in table.rows:
        cells = []
        for cell in row.cells:
            cell_text = extract_cell_text(cell)
            if cell_text.strip():
                cells.append(cell_text)
        if cells:
            rows.append(' | '.join(cells))
    return '\n'.join(rows)

def process_paragraph(paragraph: Paragraph) -> str:
    """Process a paragraph and return its text content with style information"""
    if not paragraph.text.strip():
        return ""
        
    # Check if it's a heading by looking at the style name
    style_name = paragraph.style.name.lower()
    if 'heading' in style_name:
        level = next((int(c) for c in style_name if c.isdigit()), 1)
        return f"{'#' * level} {paragraph.text}\n"
    
    # Handle other paragraph styles
    if 'list' in style_name:
        return f"• {paragraph.text}\n"
    
    return f"{paragraph.text}\n"

def load_documents_from_folder(folder_path):
    logger.debug(f"Loading documents from folder: {folder_path}")
    documents = []
    
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith('.docx') and not filename.startswith('~$'):  # Skip temp files
                doc_path = os.path.join(folder_path, filename)
                logger.debug(f"Processing document: {filename}")
                try:
                    doc = Document(doc_path)
                    content = []
                    
                    # Process paragraphs and tables in document order
                    for element in doc.element.body:
                        if isinstance(element, Paragraph):
                            text = process_paragraph(element._element)
                            if text.strip():
                                content.append(text)
                        elif isinstance(element, Table):
                            table_text = extract_table_text(element._element)
                            if table_text.strip():
                                content.append(table_text)
                    
                    # If no content was extracted using element.body, try direct access
                    if not content:
                        # Process main document paragraphs
                        for para in doc.paragraphs:
                            text = process_paragraph(para)
                            if text.strip():
                                content.append(text)
                        
                        # Process tables
                        for table in doc.tables:
                            table_text = extract_table_text(table)
                            if table_text.strip():
                                content.append(table_text)
                    
                    full_content = '\n'.join(content)
                    if full_content.strip():  # Only add document if it has content
                        documents.append({
                            'filename': filename, 
                            'content': full_content
                        })
                        logger.debug(f"Successfully processed {filename}, content length: {len(full_content)}")
                    else:
                        logger.warning(f"No content extracted from {filename}")
                except Exception as e:
                    logger.error(f"Error processing document {filename}: {str(e)}")
                    logger.exception(e)  # Log full stack trace for debugging
    except Exception as e:
        logger.error(f"Error accessing folder {folder_path}: {str(e)}")
        logger.exception(e)  # Log full stack trace for debugging
    
    logger.debug(f"Total documents loaded: {len(documents)}")
    return documents

def load_sample_documents():
    current_dir = os.path.dirname(__file__)
    docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs')
    logger.debug(f"Loading sample documents from: {docs_path}")
    return load_documents_from_folder(docs_path)