#include "be_constobj.h"

static be_define_const_map_slots(m_libjs_map) {
    { be_ckey(frame_buffer_display, -1), be_ckv_func(m_js_frame_buffer_display) },
    { be_ckey(call, 6), be_ckv_func(m_js_call) },
    { be_ckey(get_strip_size, -1), be_ckv_func(m_js_get_strip_size) },
    { be_ckey(set, -1), be_ckv_func(m_js_set) },
    { be_ckey(get_fader, -1), be_ckv_func(m_js_get_fader) },
    { be_ckey(get_brightness, -1), be_ckv_func(m_js_get_brightness) },
    { be_ckey(log, -1), be_ckv_func(m_js_log) },
    { be_ckey(get, 5), be_ckv_func(m_js_get) },
};

static be_define_const_map(
    m_libjs_map,
    8
);

static be_define_const_module(
    m_libjs,
    "js"
);

BE_EXPORT_VARIABLE be_define_const_native_module(js);
