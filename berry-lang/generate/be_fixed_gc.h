#include "be_constobj.h"

static be_define_const_map_slots(m_libgc_map) {
    { be_ckey(allocated, -1), be_ckv_func(m_allocated) },
    { be_ckey(collect, -1), be_ckv_func(m_collect) },
};

static be_define_const_map(
    m_libgc_map,
    2
);

static be_define_const_module(
    m_libgc,
    "gc"
);

BE_EXPORT_VARIABLE be_define_const_native_module(gc);
