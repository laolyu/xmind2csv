#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv
import os
from xmind2testcase.utils import get_xmind_testcase_list, get_absolute_path
from loguru import logger
"""
Convert XMind fie to Zentao testcase csv file 

Zentao official document about import CSV testcase file: https://www.zentao.net/book/zentaopmshelp/243.mhtml 
"""


def xmind_to_zentao_csv_file(xmind_file):
    """Convert XMind file to a zentao csv file"""
    xmind_file = get_absolute_path(xmind_file)
    logger.info('Start converting XMind file(%s) to zentao file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)
    # logger.info(testcases)

    fileheader = ["用例编号", "所属产品", "所属模块", "相关需求", "用例标题", "前置条件", "步骤", "预期", "实际情况",
                  "关键词", "优先级", "用例类型", "适用阶段"]
    # 用例状态、B\R\S\、结果、有谁创建、创建日期、最后修改者、修改日期、用例版本、相关用例
    zentao_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        zentao_testcase_rows.append(row)

    zentao_file = xmind_file[:-6] + '.csv'
    if os.path.exists(zentao_file):
        os.remove(zentao_file)
        # logger.info('The zentao csv file already exists, return it directly: %s', zentao_file)
        # return zentao_file

    with open(zentao_file, 'w', newline='', encoding='gbk') as f:  # encoding='utf8'
        writer = csv.writer(f)
        writer.writerows(zentao_testcase_rows)
        logger.info('Convert XMind file(%s) to a zentao csv file(%s) successfully!', xmind_file, zentao_file)

    return zentao_file


def gen_a_testcase_row(testcase_dict):
    case_no = ''
    case_product = testcase_dict['product']
    case_module = gen_case_module(testcase_dict['suite'])
    case_req = ''
    case_title = testcase_dict['name']
    case_precontion = testcase_dict['preconditions']
    case_step, case_expected_result = gen_case_step_and_expected_result(testcase_dict['steps'])
    case_real_result = ''
    case_keyword = ''
    case_priority = gen_case_priority(testcase_dict['importance'])
    case_type = gen_case_type(testcase_dict['execution_type'])
    case_stage = gen_case_stage(testcase_dict['execution_stage'])
    row = [case_no, case_product, case_module, case_req, case_title, case_precontion, case_step, case_expected_result,
           case_real_result, case_keyword, case_priority, case_type, case_stage]
    return row


def gen_case_module(module_name):
    if module_name:
        module_name = module_name.replace('（', '(')
        module_name = module_name.replace('）', ')')
    else:
        module_name = '/'
    return module_name


def gen_case_step_and_expected_result(steps):
    case_step = ''
    case_expected_result = ''

    for step_dict in steps:
        if step_dict['actions'] and not step_dict['expectedresults']:  #只有预期结果没有步骤
            case_expected_result += str(step_dict['step_number']) + '. ' + step_dict['actions'].replace('\n',
                                                                                                        '').strip() + '\n'
        else:
            case_step += str(step_dict['step_number']) + '. ' + step_dict['actions'].replace('\n', '').strip() + '\n'
            case_expected_result += str(step_dict['step_number']) + '. ' + \
                                    step_dict['expectedresults'].replace('\n', '').strip() + '\n' \
                if step_dict.get('expectedresults', '') else ''
    # logger.info(f'{steps}, {case_step}, {case_expected_result}')
    return case_step, case_expected_result

    # for step_dict in steps:
    #     case_step += str(step_dict['step_number']) + '. ' + step_dict['actions'].replace('\n', '').strip() + '\n'
    #     case_expected_result += str(step_dict['step_number']) + '. ' + \
    #                             step_dict['expectedresults'].replace('\n', '').strip() + '\n' \
    #         if step_dict.get('expectedresults', '') else ''
    # logger.info(f'{steps}, {case_step}, {case_expected_result}')
    # return case_step, case_expected_result


def gen_case_priority(priority):
    mapping = {1: '高', 2: '中', 3: '低', 4: '4'}
    if priority in mapping.keys():
        # return mapping[priority]
        return str(priority)
    else:
        # return '中'
        return '2'


def gen_case_type(case_type):
    return case_type
    # mapping = {1: '功能测试', 2: '性能测试', 3: '配置相关', 4: '安装部署', 5: '安全相关', 6: '接口测试', 7: '其他'}
    # if case_type in mapping.values():
    #     return case_type
    # else:
    #     return '功能测试'


def gen_case_stage(case_stage):
    return case_stage
    # mapping = {1: '功能测试', 2: '性能测试', 3: '配置相关', 4: '安装部署', 5: '安全相关', 6: '接口测试', 7: '其他'}
    # if case_type in mapping.values():
    #     return case_type
    # else:
    #     return '功能测试'


if __name__ == '__main__':
    xmind_file = '../docs/zentao_testcase_template.xmind'
    zentao_csv_file = xmind_to_zentao_csv_file(xmind_file)
    print('Conver the xmind file to a zentao csv file succssfully: %s', zentao_csv_file)
