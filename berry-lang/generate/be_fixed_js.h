#include "be_constobj.h"

static be_define_const_map_slots(m_libjs_map) {
    { be_const_key(frame_buffer_display, -1), be_const_func(m_js_frame_buffer_display) },
    { be_const_key(call, 6), be_const_func(m_js_call) },
    { be_const_key(get_strip_size, -1), be_const_func(m_js_get_strip_size) },
    { be_const_key(set, -1), be_const_func(m_js_set) },
    { be_const_key(get_fader, -1), be_const_func(m_js_get_fader) },
    { be_const_key(get_brightness, -1), be_const_func(m_js_get_brightness) },
    { be_const_key(log, -1), be_const_func(m_js_log) },
    { be_const_key(get, 5), be_const_func(m_js_get) },
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
