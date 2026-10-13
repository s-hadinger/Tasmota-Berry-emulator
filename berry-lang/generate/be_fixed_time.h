#include "be_constobj.h"

static be_define_const_map_slots(m_libtime_map) {
    { be_ckey(dump, 1), be_ckv_func(m_dump) },
    { be_ckey(clock, -1), be_ckv_func(m_clock) },
    { be_ckey(time, 0), be_ckv_func(m_time) },
};

static be_define_const_map(
    m_libtime_map,
    3
);

static be_define_const_module(
    m_libtime,
    "time"
);

BE_EXPORT_VARIABLE be_define_const_native_module(time);
