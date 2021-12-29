# 测试文件
from get_data import *

if __name__ == '__main__':
    data = get_input_data_list()
    class_data_lists = get_class_data_lists(data)
    # for item in class_data_lists:
    #     item.print()
    zb_list = print_class_data_lists_zb(class_data_lists)
    index = int(input("请选择数据："))
    class_data_lists = get_data_list(zb_list[index])
    zb_list = print_class_data_lists_zb(class_data_lists)

