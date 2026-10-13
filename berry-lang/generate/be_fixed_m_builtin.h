#include "be_constobj.h"

static be_define_const_map_slots(m_builtin_map) {
    { be_ckey(compile, -1), be_ckv_int(13) },
    { be_ckey(call, 16), be_ckv_int(22) },
    { be_ckey(range, 9), be_ckv_int(20) },
    { be_ckey(__iterator__, -1), be_ckv_int(16) },
    { be_ckey(real, -1), be_ckv_int(10) },
    { be_ckey(module, -1), be_ckv_int(11) },
    { be_ckey(super, -1), be_ckv_int(3) },
    { be_ckey(classname, -1), be_ckv_int(5) },
    { be_ckey(bool, -1), be_ckv_int(23) },
    { be_ckey(str, -1), be_ckv_int(8) },
    { be_ckey(list, 5), be_ckv_int(18) },
    { be_ckey(map, -1), be_ckv_int(19) },
    { be_ckey(classof, 20), be_ckv_int(6) },
    { be_ckey(isinstance, -1), be_ckv_int(15) },
    { be_ckey(size, -1), be_ckv_int(12) },
    { be_ckey(bytes, -1), be_ckv_int(21) },
    { be_ckey(assert, 4), be_ckv_int(0) },
    { be_ckey(format, -1), be_ckv_int(24) },
    { be_ckey(number, 0), be_ckv_int(7) },
    { be_ckey(issubclass, -1), be_ckv_int(14) },
    { be_ckey(open, -1), be_ckv_int(17) },
    { be_ckey(print, -1), be_ckv_int(1) },
    { be_ckey(int, -1), be_ckv_int(9) },
    { be_ckey(type, 7), be_ckv_int(4) },
    { be_ckey(input, -1), be_ckv_int(2) },
};

static be_define_const_map(
    m_builtin_map,
    25
);

static const bvalue __vlist_array[] = {
    be_const_func(be_baselib_assert),
    be_const_func(be_baselib_print),
    be_const_func(be_baselib_input),
    be_const_func(be_baselib_super),
    be_const_func(be_baselib_type),
    be_const_func(be_baselib_classname),
    be_const_func(be_baselib_classof),
    be_const_func(be_baselib_number),
    be_const_func(be_baselib_str),
    be_const_func(be_baselib_int),
    be_const_func(be_baselib_real),
    be_const_func(be_baselib_module),
    be_const_func(be_baselib_size),
    be_const_func(be_baselib_compile),
    be_const_func(be_baselib_issubclass),
    be_const_func(be_baselib_isinstance),
    be_const_func(be_baselib_iterator),
    be_const_func(be_nfunc_open),
    be_const_class(be_class_list),
    be_const_class(be_class_map),
    be_const_class(be_class_range),
    be_const_class(be_class_bytes),
    be_const_func(l_call),
    be_const_func(l_bool),
    be_const_func(be_str_format),
};

static be_define_const_vector(
    m_builtin_vector,
    __vlist_array,
    25
);
