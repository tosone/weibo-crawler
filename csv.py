import csv


class CSV():
    def __init__(self):
        pass

    def insert(self, wrote_count):
        write_info = self.get_write_info(wrote_count)
        result_headers = self.get_result_headers()
        result_data = [w.values() for w in write_info]
        with open(self.get_filepath('csv'), 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if wrote_count == 0:
                writer.writerows([result_headers])
            writer.writerows(result_data)
        print(u'%d条微博写入csv文件完毕,保存路径:' % self.got_count)
        print(self.get_filepath('csv'))
