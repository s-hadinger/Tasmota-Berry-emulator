#include "be_constobj.h"

static be_define_const_map_slots(m_libjson_map) {
    { be_ckey(dump, -1), be_ckv_func(m_json_dump) },
    { be_ckey(load, 0), be_ckv_func(m_json_load) },
};

static be_define_const_map(
    m_libjson_map,
    2
);

static be_define_const_module(
    m_libjson,
    "json"
);

BE_EXPORT_VARIABLE be_define_const_native_module(json);
