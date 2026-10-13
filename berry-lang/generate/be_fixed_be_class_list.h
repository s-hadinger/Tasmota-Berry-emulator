#include "be_constobj.h"

static be_define_const_map_slots(be_class_list_map) {
    { be_ckey(resize, 2), be_ckv_func(m_resize) },
    { be_ckey(find, -1), be_ckv_func(m_find) },
    { be_ckey(size, 16), be_ckv_func(m_size) },
    { be_ckey(_X2E_X2E, -1), be_ckv_func(m_connect) },
    { be_ckey(setitem, -1), be_ckv_func(m_setitem) },
    { be_ckey(item, 10), be_ckv_func(m_item) },
    { be_ckey(_X2Ep, -1), be_ckv_var(0) },
    { be_ckey(concat, -1), be_ckv_func(m_concat) },
    { be_ckey(reverse, -1), be_ckv_func(m_reverse) },
    { be_ckey(tostring, -1), be_ckv_func(m_tostring) },
    { be_ckey(_X3D_X3D, 21), be_ckv_func(m_equal) },
    { be_ckey(pop, -1), be_ckv_func(m_pop) },
    { be_ckey(insert, -1), be_ckv_func(m_insert) },
    { be_ckey(_X2B, -1), be_ckv_func(m_merge) },
    { be_ckey(init, -1), be_ckv_func(m_init) },
    { be_ckey(copy, 3), be_ckv_func(m_copy) },
    { be_ckey(iter, -1), be_ckv_func(m_iter) },
    { be_ckey(tobool, -1), be_ckv_func(m_tobool) },
    { be_ckey(push, -1), be_ckv_func(m_push) },
    { be_ckey(_X21_X3D, -1), be_ckv_func(m_nequal) },
    { be_ckey(clear, 17), be_ckv_func(m_clear) },
    { be_ckey(keys, -1), be_ckv_func(m_keys) },
    { be_ckey(remove, -1), be_ckv_func(m_remove) },
};

static be_define_const_map(
    be_class_list_map,
    23
);

BE_EXPORT_VARIABLE be_define_const_class(
    be_class_list,
    1,
    NULL,
    list
);
