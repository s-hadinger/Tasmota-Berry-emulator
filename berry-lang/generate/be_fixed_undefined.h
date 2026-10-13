#include "be_constobj.h"

static be_define_const_map_slots(m_libundefined_map) {
    { be_ckey(_X2Ep, -1), be_ckv_nil() },
};

static be_define_const_map(
    m_libundefined_map,
    1
);

static be_define_const_module(
    m_libundefined,
    "undefined"
);

BE_EXPORT_VARIABLE be_define_const_native_module(undefined);
