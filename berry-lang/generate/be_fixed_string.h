#include "be_constobj.h"

static be_define_const_map_slots(m_libstring_map) {
    { be_ckey(format, 12), be_ckv_func(be_str_format) },
    { be_ckey(byte, 3), be_ckv_func(str_byte) },
    { be_ckey(find, -1), be_ckv_func(str_find) },
    { be_ckey(char, 13), be_ckv_func(str_char) },
    { be_ckey(startswith, -1), be_ckv_func(str_startswith) },
    { be_ckey(split, -1), be_ckv_func(str_split) },
    { be_ckey(count, -1), be_ckv_func(str_count) },
    { be_ckey(tr, 5), be_ckv_func(str_tr) },
    { be_ckey(toupper, -1), be_ckv_func(str_toupper) },
    { be_ckey(replace, -1), be_ckv_func(str_replace) },
    { be_ckey(escape, 2), be_ckv_func(str_escape) },
    { be_ckey(tolower, 1), be_ckv_func(str_tolower) },
    { be_ckey(hex, -1), be_ckv_func(str_i2hex) },
    { be_ckey(endswith, -1), be_ckv_func(str_endswith) },
};

static be_define_const_map(
    m_libstring_map,
    14
);

static be_define_const_module(
    m_libstring,
    "string"
);

BE_EXPORT_VARIABLE be_define_const_native_module(string);
