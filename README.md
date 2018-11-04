# pdfExtraction

**Extract information from pdf files, and convert unstructured text into structured information**    
__提取 pdf 文件中的信息，将非结构化文本转化为结构化信息__  



## Feature & ToDo List

- [ ] pdf 文档中的表格提取 
  - [ ] 表格识别不全
    > 中文中有些表格没有较规范的使用表格线，因此需要通过文本对齐规律来识别，但这也可能导致目录页被识别为表格
  - [ ] 表格内换行导致的切分错误
    > 如果某一行中，具有有效值的列全部带 `\n` 换行符，则将下一行合并进来，并将下一行改为 `NaN`
  - [ ] 表格标题的提取
    > 获取表格的bbox，寻找它上面的行作为表格主题
    > 表题应该在左边或者中间，而不是右边（右边和下面一般是表中内容的注释）
  - [ ] to be added


- [ ] pdf 文档中的文字提取  
  - [ ] 文本提取取
  - [ ] 切分清洗
    - [ ] 根据句号、大量空格及换行做切分，并去除大量空格
    - [ ] to be added
  - [ ] 后处理：
    - [ ] 存放到 elasticsearch 中搜索
    - [ ] NLP etc.


- [ ] pdf 文档中的图片处理
  - [ ] 获取bbox，提取png格式图片
  - [ ] 处理图片，提取文字   
    > 根据[这篇文章](https://medium.com/@winston.smith.spb/python-ocr-for-pdf-or-compare-textract-pytesseract-and-pyocr-acb19122f38c)，考虑[PyOCR](https://gitlab.gnome.org/World/OpenPaperwork/pyocr) + [tesseract + LSTM](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files)
  - 返回上面的文本处理和图片处理部分
  

### Note
- [tesseract](https://github.com/tesseract-ocr/tesseract) 是一个惠普、谷歌多年前开源，成熟且稳定更新的 OCR 工具库，
  可以使用[ImageMagick](https://github.com/ImageMagick/ImageMagick)提取扫描图片然后由其识别

- [xpdf](https://www.xpdfreader.com/) 项目提供了较为成熟稳定的文本pdf转换为纯文本的途径


## Related Projects / 相关项目


- [xpdf](https://www.xpdfreader.com/)
  *Xpdf is a free PDF viewer and toolkit, including a text extractor, image 
  converter, HTML converter, and more.*

- [tika](https://tika.apache.org/contribute.html)
  *detects and extracts metadata and text from over a thousand different file 
  types (such as PPT, XLS, and PDF). *

- [tika-python](https://github.com/chrismattmann/tika-python)
  *A Python port of the Apache Tika library that makes Tika available using 
  the Tika REST Server.*
  
- [tabula-py](https://github.com/chezou/tabula-py)
  *Simple wrapper of tabula-java: extract table from PDF into pandas DataFrame*

- [pdfminer/pdfminer.six](https://github.com/pdfminer/pdfminer.six)  
  *Python PDF Parser*
  
- [PyPDF2](https://github.com/mstamy2/PyPDF2)  
  *A utility to read and write PDFs with Python*
  
- [pdfplumber](https://github.com/jsvine/pdfplumber)
  *Plumb a PDF for detailed information about each char, rectangle, line, et cetera — and easily extract text and tables.*
  
- [pdftabextract](https://github.com/WZBSocialScienceCenter/pdftabextract)  
  *A set of tools for extracting tables from PDF files helping to do data mining on (OCR-processed) scanned documents.*
  
- [OCRmyPDF](https://github.com/jbarlow83/OCRmyPDF)   
  *OCRmyPDF adds an OCR text layer to scanned PDF files, allowing them to be searched*
  
- [tesseract](https://github.com/tesseract-ocr/tesseract)
  *Tesseract Open Source OCR Engine (main repository)*
  
  
## Reference / 参考资料
- [Programming with PDFMiner](https://euske.github.io/pdfminer/programming.html)

- [DATA MINING PDFS – THE SIMPLE CASES
  ](https://datascience.blog.wzb.eu/2017/02/16/data-mining-ocr-\
  pdfs-using-pdftabextract-to-liberate-tabular-data-from-scanned-documents/)

- [DATA MINING OCR PDFS — USING PDFTABEXTRACT TO LIBERATE TABULAR DATA FROM 
  SCANNED DOCUMENTS](https://datascience.blog.wzb.eu/2017/02/16/data-mining-ocr-pdfs-\
  using-pdftabextract-to-liberate-tabular-data-from-scanned-documents/)

- [StackOverflow:how-to-extract-text-from-a-pdf-file](https://stackoverflow\
  .com/questions/34837707/how-to-extract-text-from-a-pdf-file)

- [Python: OCR for PDF or Compare textract, pytesseract, and pyocr](https://medium.com/@winston.smith.spb/python-ocr-for-pdf-or-compare-textract-pytesseract-and-pyocr-acb19122f38c)
