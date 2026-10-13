#include "be_constobj.h"

static be_define_const_map_slots(be_class_re_pattern_map) {
    { be_ckey(searchall, 4), be_ckv_func(re_pattern_search_all) },
    { be_ckey(matchall, -1), be_ckv_func(re_pattern_match_all) },
    { be_ckey(match, -1), be_ckv_func(re_pattern_match) },
    { be_ckey(match2, 2), be_ckv_func(re_pattern_match2) },
    { be_ckey(split, -1), be_ckv_func(re_pattern_split) },
    { be_ckey(_p, -1), be_ckv_var(0) },
    { be_ckey(search, 5), be_ckv_func(re_pattern_search) },
};

static be_define_const_map(
    be_class_re_pattern_map,
    7
);

BE_EXPORT_VARIABLE be_define_const_class(
    be_class_re_pattern,
    1,
    NULL,
    re_pattern
);
