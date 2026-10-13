#include "be_constobj.h"

static be_define_const_map_slots(m_libintrospect_map) {
    { be_ckey(fromptr, 9), be_ckv_func(m_fromptr) },
    { be_ckey(set, 8), be_ckv_func(m_setmember) },
    { be_ckey(name, 10), be_ckv_func(m_name) },
    { be_ckey(setmodule, -1), be_ckv_func(m_setmodule) },
    { be_ckey(module, -1), be_ckv_func(m_getmodule) },
    { be_ckey(get, 7), be_ckv_func(m_findmember) },
    { be_ckey(ismethod, -1), be_ckv_func(m_ismethod) },
    { be_ckey(toptr, -1), be_ckv_func(m_toptr) },
    { be_ckey(solidified, -1), be_ckv_func(m_solidified) },
    { be_ckey(members, -1), be_ckv_func(m_attrlist) },
    { be_ckey(contains, -1), be_ckv_func(m_contains) },
};

static be_define_const_map(
    m_libintrospect_map,
    11
);

static be_define_const_module(
    m_libintrospect,
    "introspect"
);

BE_EXPORT_VARIABLE be_define_const_native_module(introspect);
