#include "be_constobj.h"

static be_define_const_map_slots(be_class_range_map) {
    { be_ckey(__lower__, 8), be_ckv_var(0) },
    { be_ckey(__incr__, -1), be_ckv_var(2) },
    { be_ckey(setrange, -1), be_ckv_func(m_setrange) },
    { be_ckey(__upper__, -1), be_ckv_var(1) },
    { be_ckey(init, -1), be_ckv_func(m_init) },
    { be_ckey(tostring, 4), be_ckv_func(m_tostring) },
    { be_ckey(incr, -1), be_ckv_func(m_incr) },
    { be_ckey(upper, 6), be_ckv_func(m_upper) },
    { be_ckey(lower, -1), be_ckv_func(m_lower) },
    { be_ckey(iter, -1), be_ckv_func(m_iter) },
};

static be_define_const_map(
    be_class_range_map,
    10
);

BE_EXPORT_VARIABLE be_define_const_class(
    be_class_range,
    3,
    NULL,
    range
);
