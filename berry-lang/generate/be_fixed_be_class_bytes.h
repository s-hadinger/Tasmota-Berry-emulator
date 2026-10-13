#include "be_constobj.h"

static be_define_const_map_slots(be_class_bytes_map) {
    { be_ckey(asstring, -1), be_ckv_func(m_asstring) },
    { be_ckey(appendb64, 9), be_ckv_func(m_appendb64) },
    { be_ckey(_buffer, -1), be_ckv_func(m_buffer) },
    { be_ckey(resize, 38), be_ckv_func(m_resize) },
    { be_ckey(_X2Elen, 20), be_ckv_var(1) },
    { be_ckey(ismapped, 32), be_ckv_func(m_is_mapped) },
    { be_ckey(size, 0), be_ckv_func(m_size) },
    { be_ckey(reverse, 3), be_ckv_func(m_reverse) },
    { be_ckey(copy, 35), be_ckv_func(m_copy) },
    { be_ckey(getfloat, 22), be_ckv_func(m_getfloat) },
    { be_ckey(getbits, -1), be_ckv_func(m_getbits) },
    { be_ckey(_X3D_X3D, -1), be_ckv_func(m_equal) },
    { be_ckey(fromhex, -1), be_ckv_func(m_fromhex) },
    { be_ckey(set, -1), be_ckv_func(m_set) },
    { be_ckey(setitem, -1), be_ckv_func(m_setitem) },
    { be_ckey(_X2E_X2E, -1), be_ckv_func(m_connect) },
    { be_ckey(fromb64, -1), be_ckv_func(m_fromb64) },
    { be_ckey(setfloat, -1), be_ckv_func(m_setfloat) },
    { be_ckey(addfloat, -1), be_ckv_func(m_addfloat) },
    { be_ckey(appendhex, 24), be_ckv_func(m_appendhex) },
    { be_ckey(add, -1), be_ckv_func(m_add) },
    { be_ckey(_change_buffer, -1), be_ckv_func(m_change_buffer) },
    { be_ckey(setbits, -1), be_ckv_func(m_setbits) },
    { be_ckey(get, -1), be_ckv_func(m_getu) },
    { be_ckey(setbytes, -1), be_ckv_func(m_setbytes) },
    { be_ckey(isreadonly, -1), be_ckv_func(m_is_readonly) },
    { be_ckey(clear, 27), be_ckv_func(m_clear) },
    { be_ckey(tob64, -1), be_ckv_func(m_tob64) },
    { be_ckey(_X2B, 19), be_ckv_func(m_merge) },
    { be_ckey(tobool, -1), be_ckv_func(m_tobool) },
    { be_ckey(geti, -1), be_ckv_func(m_geti) },
    { be_ckey(tostring, -1), be_ckv_func(m_tostring) },
    { be_ckey(deinit, -1), be_ckv_func(m_deinit) },
    { be_ckey(init, 16), be_ckv_func(m_init) },
    { be_ckey(_X2Esize, -1), be_ckv_var(2) },
    { be_ckey(fromstring, -1), be_ckv_func(m_fromstring) },
    { be_ckey(seti, 29), be_ckv_func(m_set) },
    { be_ckey(_X21_X3D, 25), be_ckv_func(m_nequal) },
    { be_ckey(append, 39), be_ckv_func(m_connect) },
    { be_ckey(_X2Ep, -1), be_ckv_var(0) },
    { be_ckey(item, 5), be_ckv_func(m_item) },
    { be_ckey(tohex, 10), be_ckv_func(m_tohex) },
};

static be_define_const_map(
    be_class_bytes_map,
    42
);

BE_EXPORT_VARIABLE be_define_const_class(
    be_class_bytes,
    3,
    NULL,
    bytes
);
