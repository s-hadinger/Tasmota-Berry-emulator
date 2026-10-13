#include "be_constobj.h"

static be_define_const_map_slots(m_libsolidify_map) {
    { be_ckey(compact, -1), be_ckv_func(m_compact) },
    { be_ckey(dump, -1), be_ckv_func(m_dump) },
    { be_ckey(nocompact, 1), be_ckv_func(m_nocompact) },
};

static be_define_const_map(
    m_libsolidify_map,
    3
);

static be_define_const_module(
    m_libsolidify,
    "solidify"
);

BE_EXPORT_VARIABLE be_define_const_native_module(solidify);
