from tinygrad import TinyJit

@TinyJit
def f(tg_out, tg_data):
    return tg_out.assign(tg_data[:, :, 0] * 0.2989 + tg_data[:, :, 1] * 0.587 + tg_data[:, :, 2] * 0.114).realize()