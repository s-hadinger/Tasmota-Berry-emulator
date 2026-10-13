#include "be_constobj.h"

static be_define_const_map_slots(m_libre_map) {
    { be_ckey(matchall, -1), be_ckv_func(be_re_match_all) },
    { be_ckey(searchall, -1), be_ckv_func(be_re_search_all) },
    { be_ckey(compilebytes, 5), be_ckv_func(be_re_compilebytes) },
    { be_ckey(split, -1), be_ckv_func(be_re_split) },
    { be_ckey(match, 2), be_ckv_func(be_re_match) },
    { be_ckey(search, -1), be_ckv_func(be_re_search) },
    { be_ckey(compile, -1), be_ckv_func(be_re_compile) },
    { be_ckey(match2, -1), be_ckv_func(be_re_match2) },
    { be_ckey(dump, -1), be_ckv_func(be_re_dump) },
};

static be_define_const_map(
    m_libre_map,
    9
);

static be_define_const_module(
    m_libre,
    "re"
);

BE_EXPORT_VARIABLE be_define_const_native_module(re);
