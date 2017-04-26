#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import base64
from wx.lib.embeddedimage import PyEmbeddedImage
# INSERT_START
m_exit = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/AAAA"
    "CXBIWXMAAA3WAAAN1gGQb3mcAAAACXZwQWcAAAAQAAAAEABcxq3DAAACJElEQVQ4y8WTsUtb"
    "URTGf/e+l5iEqNFCK5Y0DpZCJIKbi+Aggl3tJDgUBBeHbG6Kk3MdSgdx76QuIt3aUUEcpCg4"
    "mEYliaEJkry85L17T4eo1L/AD854vvP7Pjjw0lLflGL57Iwf+fynoWz2oxKxAIgg1oK1oDWI"
    "dEdrXbu5+f1zb+/LG6UCF4BslmgiMek2m5/F97vLQUAylyMxOkr14ADbanUvOg7RSOSXC1+B"
    "QD+xWIttt7GtFmIMiQ8f6B0fJzU1RXJsjMjAALbVwvo+GCOPa88MJAwBeD0/z/DyMk4yiRhD"
    "3+QkmdVVYpkM0ukgxqCeGQQBIoJ0OiRzOQZnZqju7uIXCmAt1f19rO8ztLCAdt1uLw/qdtBu"
    "PxH0TkzgF4v8PTwkkkrRPD2lcXREJRbjbT6PG49jK5UnAveRAGtRxuDE44S1Gp1CAe/4GNNo"
    "IL5PpK8PjCEoFgnrdbTjgLUPETodlAjieTRPToil0zhKEVYq4Hk4SjE4O0t4d4e9vsbRGlHq"
    "P4KLC6znERSLVC4vSU1P8357m9LWFmG5TGpujleLi5Q2NpBSCd3fj30W4fwcaTTg/h5Tr/Nn"
    "aYnhtTXebW6iHAdTrVJZX6e+s4MLOEohzwxcF6UUkWQSrCW8uuJ6ZYWeTAadSBDe3mJKJdye"
    "HnQ0iuc4mDAEpboGtXKZljHfw2z2QosIgBEhCAIQQaXTqJGRbvNaK69evzHQfuk/7OofflgO"
    "ZQ3sgX8AAAAldEVYdGRhdGU6Y3JlYXRlADIwMTAtMDUtMjRUMDc6NDI6MTgtMDY6MDCB1lnq"
    "AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDEwLTA1LTI0VDA3OjQyOjE4LTA2OjAw8IvhVgAAADV0"
    "RVh0TGljZW5zZQBodHRwOi8vY3JlYXRpdmVjb21tb25zLm9yZy9saWNlbnNlcy9MR1BMLzIu"
    "MS87wbQYAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAA90RVh0U291"
    "cmNlAG51b3ZlWFQy6iA23AAAACJ0RVh0U291cmNlX1VSTABodHRwOi8vbnVvdmV4dC5wd3Nw"
    "Lm5ldJGJxy0AAAAASUVORK5CYII="
)
m_open = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/AAAA"
    "CXBIWXMAAA3WAAAN1gGQb3mcAAAACXZwQWcAAAAQAAAAEABcxq3DAAAB/UlEQVQ4y6WTz0tU"
    "URTHP/fduWMFpln+qBHKTYsggqAggiAI2rUpAoOgRVRCEUHuon2LcFGb6AdaQf+AVBQlKIoS"
    "Bi5aZBahCA7OZOPUzLvvvXtPixrxOURRB87iXDgfvt9zz1Eiwv9EZnXRfbG3v21zyw4RwTlH"
    "FEVYa4mTZFPZRv2D92/3rQUoEWHgin6cJL77U9O54ML5azjncM5hraVYLDIx9Y6FpeXK1MyH"
    "Ey8H7j6rUxAn/tSxwzn15PM6tNYMjU+SLxSpKckXlug5fXLDnYePnt7saabZlCKt1Y0zff56"
    "zYJyThABrTVHDu5fUeGc4+PsPEOjE+S2dvK+dJzevYPZkbeLV4EVAFXrEVFkMhlejb0hXyji"
    "vUdE8N6Ta9/Cnp1dlOeHCVSA97I+NcTQerwXtNYcPXQgpWB16oyhal39L4ShQ1BorXkxMs7C"
    "YiGloLOjlX27d6F1htD6esBcvkJT8pzhB5OYylfawxJRWCa230CEcLqB0bEGOhLHdDlCa50G"
    "NLdtp7OxkWwDGNOKMdsw2SzGGAD8KhtxHDMy9DoN6OrKrVkRB65K7KqpV60gMFJvwVZKf7m8"
    "gsjPTAHi6pd/vwUdKL+YXwhamsxfNX2vOoJAyQrAeembmatcltn0cf0ulAJgEn4dUy3uXVIb"
    "geAP/f7sLVmuFT8AlKcVk7MTecQAAAAldEVYdGRhdGU6Y3JlYXRlADIwMTAtMDUtMjRUMDc6"
    "Mzg6MDUtMDY6MDASsr3+AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDEwLTA1LTI0VDA3OjM4OjA1"
    "LTA2OjAwY+8FQgAAADZ0RVh0TGljZW5zZQBodHRwOi8vY3JlYXRpdmVjb21tb25zLm9yZy9s"
    "aWNlbnNlcy9ieS1zYS8zLjAvYeyvUQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9y"
    "Z5vuPBoAAAAWdEVYdFNvdXJjZQBlY2hvLWljb24tdGhlbWWpTLdTAAAANHRFWHRTb3VyY2Vf"
    "VVJMAGh0dHBzOi8vZmVkb3JhaG9zdGVkLm9yZy9lY2hvLWljb24tdGhlbWUviDIuQwAAAABJ"
    "RU5ErkJggg=="
)
m_settings = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAAAZi"
    "S0dEAAAAAAAA+UO7fwAAAAlwSFlzAAAASAAAAEgARslrPgAAAAl2cEFnAAAAEAAAABAAXMat"
    "wwAAA6JJREFUOMtlk+9PGwUcxr/t9XpX7nq9g+tPSktLVwalwlyQsXVbINGx6DQxxr0x/piv"
    "SDQxRqMviK/2Rmd8KYmJxphMsyWiIWa+0ZmldekgrORIgY6Wge3Wu0K53tFy13J39YUxkfn8"
    "AZ/n8+J5TAAAMHELRmKduN1hZZN3y7tvvNx32tFh6uGyxd97PM5SXWnB7Z9vgJT5HJ6MBc7N"
    "AzSNjjPDXW8lhjovXDjBZkI+8ixNtKOaXLb+cfvBj4d2Rr36xbWDdyf+D0Bg9xyA3xHx+qnP"
    "pp5xJ/r81BmbzRrGcYwiKXs4Gg+e97msoW9mv7s/ffnpViqVOmpw/NVYZPKU70qgm3I1Ds3t"
    "pZWKuLhRqztZypmIu2JhxhzbKT/yDrmqPzWkvVUA0I4YWGNXXjve3/XBWNzZuSMq0s0f5j+p"
    "bixct6JYRDSoIEFioEl7tvEBpq+xLz78+KMPS5cuvQherxcWFhbAUt19vPtLUi8SFEEFWQw6"
    "SYt1YhC/eOq8P/7rQwPkQwug3f1Mdcc8xbKb69ls1lCbLZAkKQMALUTXQpuMv88e7fclKNre"
    "gRLMsFBVxjTMRak2J0gaApslCViQkKnTfUPhcPglt9v9bLFYXE2n01tmQOKIgZLeQvkAubcu"
    "tjW7x9sx/DyZM/dCDSGAL4vtYnJ+v1X6s9VuGw6WZXsURekSBIGYmZkBBNgXDtsY0hBK27Vq"
    "qdjWbZ09qI0wCWUR9hoGyDX5cWX5t2tYg8vhto5Bj8eDbW9vbxUKhZuZTGYHAfaVdjP93l/W"
    "/PVUN8uQksGcRJW6bdIjmhp8Sbh/b/nT3J3sV4jGcZFj0dFgMBiiaZpmGCbE8/yGBR68DkBf"
    "NsRasV6vrH3rxg+pyaGz7z93Yph4ytcwD1p2UXnIH9aN7lAoFHLoug6KomCqqvarqmq3AABA"
    "7Qa8edEP6U3bQSwQoaMBEm8cNMBB2Z1j4+Mzsiy/jaIoSdO0VxRFPZVKPVpbW7vFcVwW+XcQ"
    "y3kZ/D0BlCTtCVneH8jn84okSZjP57MRBMGqqkppmmZWVRWWlpa+n5ubu8rzfNny31Xpun4g"
    "CMKXPM9nNE3DRkZG3nG5XCebzabCcRzPsqwHAPZ5nl+VZbmCIIhxBLCysgKzs7Nb09PTWwCA"
    "u91uTzKZJCuVyt1cLvd1IBBISJIkcBw3/0+fDqYn3zUwMACSJEG9Xjf19vY6cRw/Vq1Wq4VC"
    "YR0AMADQR0dHtcXFRQAA+Btq5qX4WNtumwAAACV0RVh0Y3JlYXRlLWRhdGUAMjAwOS0xMS0x"
    "NVQxNjowODo0NC0wNzowMHaWzkcAAAAldEVYdGRhdGU6Y3JlYXRlADIwMTAtMDEtMjVUMDg6"
    "MzA6MjUtMDc6MDCbjNRUAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDEwLTAxLTExVDA5OjE4OjM0"
    "LTA3OjAwkYpQcQAAADV0RVh0TGljZW5zZQBodHRwOi8vY3JlYXRpdmVjb21tb25zLm9yZy9s"
    "aWNlbnNlcy9MR1BMLzIuMS87wbQYAAAAJXRFWHRtb2RpZnktZGF0ZQAyMDA5LTExLTE1VDE2"
    "OjA4OjQ0LTA3OjAwKSe4cwAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwA"
    "AAANdEVYdFNvdXJjZQBOdXZvbGGsTzXxAAAANHRFWHRTb3VyY2VfVVJMAGh0dHA6Ly93d3cu"
    "aWNvbi1raW5nLmNvbS9wcm9qZWN0cy9udXZvbGEvdj20UgAAAABJRU5ErkJggg=="
)
m_title = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/AAAA"
    "CXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAAQAAAAEABcxq3DAAACPklEQVQ4y6WTy0tV"
    "URTGf2vvfW5SlnI1KzIhg7qRZpT0EiIhp9GwQeMgmjRp0rB/oEFB0KwggmgS0YMeOikLNEXB"
    "qwmaPTSs64Nzw9O995y9Glw1ehBJi7XZ32Kt/a31sdiiqvyPuVv3u7KrXJABxKOU6bTs5QtZ"
    "LDZGEJFyLILXZNQVYl+3f2+zABTiGO8VRIhLigp4wABiwIghsBAIWGt42T+40SUYnwu/ApAk"
    "HlRJ4hI2CFCvOGOI4xJiHcYaioUizjkQKHnxTkVqJifeArBSCSpSxfVH3YkuWmfPsK4E3+7s"
    "9YZ/WIL6hO4XT8g+ugTAWM+VpQRy48HzpH59jfkbQX6qj+Mda8hNjfF6oplU1RYAcmGoRlHa"
    "WzO0t2YAfsOHMhtYF3XDt/fUpgOSQp4jexppb82gAs5a+8euMnqNgY+O1UHI0YNrIXwPPk2T"
    "PGPg5jOqa2pJ5StxItDVO7L8cAlXLgzR0rYbWFtOhPPg52nYKDSsDgmzfcxqB857vzxyV+/I"
    "Mn4Ynmeg8ypNdZPYhubFPQJzWWYmE760nKXa78JYRKIoIoqinyRUrKsnSG/Fzn6GmeEf58MU"
    "05VtZA6fAlWcMRq/GnoX/CoBYGg8z47tdViAgXFoaSRJ1zE0mme6dwRRTdzsTO5eKinuQ9lc"
    "TGL1Hrz3KJBSNXaNs3efVjCTOubTTyY50YHZOd+jbz69i2aj0mP523e+dSZ1Ogrtjv65b5cv"
    "P9CJcyekYlulPbnJ2AODC8ULF+/o3HdAEz+jeQNrzQAAACV0RVh0Y3JlYXRlLWRhdGUAMjAw"
    "OS0xMS0yOFQxNzoxODoyOC0wNzowMDGRsiwAAAAldEVYdGRhdGU6Y3JlYXRlADIwMTAtMDIt"
    "MjBUMjM6MjQ6MjAtMDc6MDDeeaT4AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDEwLTAxLTExVDA4"
    "OjQyOjQwLTA3OjAw1OOYdQAAADV0RVh0TGljZW5zZQBodHRwOi8vY3JlYXRpdmVjb21tb25z"
    "Lm9yZy9saWNlbnNlcy9MR1BMLzIuMS87wbQYAAAAJXRFWHRtb2RpZnktZGF0ZQAyMDA5LTEx"
    "LTI4VDE0OjMxOjI3LTA3OjAwgdtKNAAAABZ0RVh0U291cmNlAENyeXN0YWwgUHJvamVjdOvj"
    "5IsAAAAndEVYdFNvdXJjZV9VUkwAaHR0cDovL2V2ZXJhbGRvLmNvbS9jcnlzdGFsL6WRk1sA"
    "AAAASUVORK5CYII="
)

# INSERT_END
def image2base64(path):
    icon = open(path, 'rb')
    iconData = icon.read()
    iconData = base64.b64encode(iconData)
    LIMIT = 72
    liIcon = []
    fn = os.path.basename(path).split(".")[0]
    liIcon.append("{} = PyEmbeddedImage(".format(fn))
    while True:
        sLimit = iconData[:LIMIT]
        iconData = iconData[LIMIT:]
        liIcon.append('    \"%s\"' % sLimit)
        if len(sLimit) < LIMIT:
            break
    liIcon.append(")")
    return '\n'.join(liIcon)

def insert2file(str, res_path, startstr, endstr):
    fp = file(res_path)
    s = fp.read()
    fp.close()
    a = s.split('\n')
    idx_s = a.index(startstr)
    idx_e = a.index(endstr)
    s = '\n'.join(a[:idx_s+1]) + '\n'+str+'\n' + '\n'.join(a[idx_e:])
    fp = file(res_path, 'w')
    fp.write(s)
    fp.close()

if __name__ == '__main__':
    import sys
    from os import listdir
    from os.path import isfile, join

    dir_path = sys.argv[1]
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    str_buf = ""
    for f in files:
        p = join(dir_path, f)
        str_buf += image2base64(p) + '\n'
    res_file = sys.argv[0]
    insert2file(str_buf, res_file, "# INSERT_START", "# INSERT_END")






