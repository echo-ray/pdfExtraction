import os
import tabula
import pdfplumber
from pprint import pprint
import pandas as pd
import numpy as np
import zipfile



def extratPDF(file_path, table_method='pdfplumber', text_method='pdfplumber'):
    '''先获取表格，然后处理句子
       table_method 可选 'tabula', 'pdfplumber', None
       text_method 可选 'pdfplumber', 'pdfminer', None
    '''
    if not os.path.isfile(file_path):
        print(f'file {file_path} not found')
        return None
    
    info = {'tables':[], 'text':[]}
    pdf = pdfplumber.open(file_path)   
    # 处理表格
    if table_method is None:
        pass
    elif table_method == 'pdfplumber':
        info['tables'] = extract_table_by_pdfplumber(pdf, text_tolerance=2)
    elif table_method == 'tabula':
        info['tables'] = extract_table_by_tabula(file_path)
    else:
        print(f'other table extract method {table_method} has not implement yet')
    if info['tables']:
        for i,table in enumerate(info['tables']):
            info['tables'][i] = process_raw_table(table)
            
    # 处理句子
    if text_method is None:
        pass
    elif text_method == 'pdfplumber':
        info['text'] = extract_text_by_pdfplumber(pdf)
    else:
        print(f'other text extract method {text_method} has not implement yet')
    if info['text']:
        info['text'] = process_raw_text(info['text'])
    
    return info



def convert2csv(file_path, compress=False):
    '''提取pdf中的表格并保存在文件同名目录下
       每个 DataFrame 输出一个 csv 文件
    '''
    pdf_info = extratPDF(
        file_path, 
        table_method='pdfplumber', 
        text_method=None)
    tables = pdf_info['tables']
    
    csv_path = file_path.replace('.PDF','').replace('.pdf', '') 
    if compress:
        zip_file = zipfile.ZipFile(csv_path + '.zip', 'w')
    if not os.path.exists(csv_path):
        print(csv_path)
        os.makedirs(csv_path)
    for i, table in enumerate(tables):
        table.to_csv(f'{csv_path}{os.sep}{i+1}.csv', 
                     index=False, header=False,
                     encoding='gbk')
        if compress:
            zip_file.write(
                f'{csv_path}{os.sep}{i+1}.csv',
                f'{os.path.split(csv_path)[-1]}{os.sep}{i+1}.csv')
    if compress:
        zip_file.close()
        return csv_path + '.zip'
    return csv_path + os.sep


def convert2excel(file_path, save_path=None):
    '''提取pdf中的表格并保存为 excel文件
       每个DataFrame一个Sheet
    '''
    pdf_info = extratPDF(
        file_path, 
        table_method='pdfplumber', 
        text_method=None)
    tables = pdf_info['tables']
    
    excel_path = file_path.replace('.PDF','').replace('.pdf', '')
    with pd.ExcelWriter(excel_path + '.xlsx') as excel:
        for i, table in enumerate(tables):
            table.to_excel(excel, f'Sheet{i+1}')
    return excel_path + '.xlsx'


def extract_text_by_pdfplumber(file, **kargs):
    # 处理文本，返回句子等
    if isinstance(file, str):
        pages = pdfplumber.open(file).pages
    if isinstance(file, pdfplumber.pdf.PDF):
        pages = file.pages
        
    text = [[]]
    for page in pages:
        x0,y0 = Decimal(0), Decimal(0)
        for char in page.chars:
            if (char['x0'] < x0-20) and (char['y0'] < y0-20):
                print('case 1', char['text'])
                x0, y0 = char['x0'], char['y0']
                text.append([char['text']])
            elif (char['x0'] > x0+1) and (char['y0'] > y0+1):
                x0, y0 = char['x0'], char['y0']
                text.append([char['text']])
                print('case 2', char['text'])
            else:
                text[-1].append(char['text'])
                # print(char['text'], end='')
        # raw_text = [char['text'] for char in page.chars]
        # text.extend(raw_text)
    return text


def extract_table_by_tabula(file_path, page='all'):
    '''使用 tabula-java输出的json数据来提取表格'''
    tables = []
    try:
        tables = tabula.read_pdf(
            file_path,
            encoding='utf-8', 
            pages='all',
            multiple_tables=True
        )
    except Exception as e:
        print('Error in extract_table_by_tabula:', e)
    finally:
        return tables


def extract_table_by_pdfplumber(file, text_tolerance=2):
    '''使用 pdfplumber 的两种分析模式来获取表格
    '''
    if isinstance(file, str):
        pages = pdfplumber.open(file).pages
    if isinstance(file, pdfplumber.pdf.PDF):
        pages = file.pages
    tables = []
    for page in pages:
        raw_tables = pdfplumber_by_line(page)
        if not raw_tables:
            raw_tables = pdfplumber_by_text(
                page, text_tolerance=2)
        if not raw_tables:
            continue
        for raw_table in raw_tables:
            raw_table_ = raw_table.extract()
            pd_table = pd.DataFrame(raw_table_)
            # 有时会将较为整齐的文本当成表格，去掉这种 1*x 或 x*1的不正确的表格
            if 1 in list(pd_table.shape):
                continue
            tables.append(pd_table
                # 'bbox':raw_table.bbox
            )
    return tables


def pdfplumber_by_line(page):
    # 根据pdf中的线条来拆分表格，一般比较精准
    tables = page.find_tables(table_settings={
        "vertical_strategy": "lines", 
        "horizontal_strategy": "lines",
        "intersection_tolerance": 2,
    })
    return tables

def pdfplumber_by_text(page, text_tolerance=1):
    # 根据pdf页中的文本对齐来拆分表格，结果会更全，但不一定正确
    tables = page.find_tables(table_settings={
        "vertical_strategy": "text", 
        "horizontal_strategy": "text",
        # "intersection_tolerance": 2,
        "text_tolerance": text_tolerance,
        # "text_x_tolerance": 1, # pixels
        # "text_y_tolerance": 5,
    })
    return tables

def pdfplumber_find_title(page, bbox):
    # 根据表格的bbox位置，来查找它上面的标题
    pass

def process_raw_text(text, split=['。', '/n']):
    '''处理文本：切分句子和表格的行，存储到es等
    '''
    pass


def process_raw_table(table, drop_column_ratio=0.1, drop_row_ratio=0.1):
    '''处理原始的表格，删除空白行等 
    '''
    if isinstance(table, list):
        table = pd.DataFrame(table)
    
    # 将 None 和 空白字符 替换成 NaN
    table = table.applymap(lambda x:x if x else np.NaN)
    # 删除全部是空或者90%是空的行、列
    # column_valid_ratio = table.count(axis=0)/table.shape[0]
    # table = table.T[column_valid_ratio > drop_column_ratio].T
    # row_valid_ratio = table.count(1)/table.shape[1]
    # table = table[row_valid_ratio > drop_row_ratio]
    
    # 删除全部是空的行和列
    table.dropna(axis=0, how='all', inplace=True)
    table.dropna(axis=1, how='all', inplace=True)
    
    # 将大量空白符以及换行符等，替换成单个空白符
    table.replace(regex=r'(：)', value=': ', inplace=True)
    # 数字里的逗号会产生干扰
    table.replace(regex=r'(,)', value='',inplace=True)
    table.replace(regex=[r'(\n)', r'(  )'], value=' ', inplace=True)
    
    return table



if __name__ == '__main__':
    # file_path = input('请输入pdf文件目录')
    # if not file_path:
    # file_path = './data/tianma_season_1.pdf'
    file_path = './data/tianma.pdf'
    # file_path = './data/浦发银行半年报.PDF'
    convert2csv(file_path,compress=True)
    convert2excel(file_path)
