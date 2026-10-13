#include "be_constobj.h"

static be_define_const_map_slots(be_class_map_map) {
    { be_ckey(setitem, -1), be_ckv_func(m_setitem) },
    { be_ckey(remove, -1), be_ckv_func(m_remove) },
    { be_ckey(insert, -1), be_ckv_func(m_insert) },
    { be_ckey(tostring, 4), be_ckv_func(m_tostring) },
    { be_ckey(has, -1), be_ckv_func(m_contains) },
    { be_ckey(init, -1), be_ckv_func(m_init) },
    { be_ckey(contains, 9), be_ckv_func(m_contains) },
    { be_ckey(_X2Ep, 13), be_ckv_var(0) },
    { be_ckey(tobool, -1), be_ckv_func(m_tobool) },
    { be_ckey(size, -1), be_ckv_func(m_size) },
    { be_ckey(find, -1), be_ckv_func(m_find) },
    { be_ckey(keys, -1), be_ckv_func(m_keys) },
    { be_ckey(item, -1), be_ckv_func(m_item) },
    { be_ckey(iter, -1), be_ckv_func(m_iter) },
};

static be_define_const_map(
    be_class_map_map,
    14
);

BE_EXPORT_VARIABLE be_define_const_class(
    be_class_map,
    1,
    NULL,
    map
);
