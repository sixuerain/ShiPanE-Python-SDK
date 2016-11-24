import shipane_sdk


# 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 定义一个全局变量, 保存要操作的股票
    # 000001(股票:平安银行)
    g.security = '000001.XSHE'
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')


def process_initialize(context):
    # 创建 JoinQuantExecutor 对象
    # 可选参数包括：host, port, title, account 等
    g.__executor = shipane_sdk.JoinQuantExecutor(host='xxx.xxx.xxx.xxx')


# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    # 保存 order 对象
    current_order = order('000001.XSHE', 100)
    log.info('JointQuant executed:\n%s', str(current_order))

    # 实盘易依据聚宽的 order 对象下单
    response = g.__executor.execute(current_order)
    if response is not None:
        log.info('ShiPanE response:\nstatus_code: %d\ntext: %s', response.status_code, response.text)
    else:
        log.error('ShiPanE did not response')

    current_order = order(g.security, -100)
    g.__executor.execute(current_order)

    # 撤单
    g.__executor.cancel(current_order)
