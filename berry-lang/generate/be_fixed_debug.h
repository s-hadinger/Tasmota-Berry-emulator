#include "be_constobj.h"

static be_define_const_map_slots(m_libdebug_map) {
    { be_ckey(upvname, -1), be_ckv_func(m_upvname) },
    { be_ckey(gcdebug, -1), be_ckv_func(m_gcdebug) },
    { be_ckey(codedump, -1), be_ckv_func(m_codedump) },
    { be_ckey(allocs, -1), be_ckv_func(m_allocs) },
    { be_ckey(traceback, -1), be_ckv_func(m_traceback) },
    { be_ckey(calldepth, 8), be_ckv_func(m_calldepth) },
    { be_ckey(attrdump, 7), be_ckv_func(m_attrdump) },
    { be_ckey(top, -1), be_ckv_func(m_top) },
    { be_ckey(frees, -1), be_ckv_func(m_frees) },
    { be_ckey(varname, -1), be_ckv_func(m_varname) },
    { be_ckey(reallocs, 1), be_ckv_func(m_reallocs) },
    { be_ckey(counters, 9), be_ckv_func(m_counters) },
    { be_ckey(caller, -1), be_ckv_func(m_caller) },
};

static be_define_const_map(
    m_libdebug_map,
    13
);

static be_define_const_module(
    m_libdebug,
    "debug"
);

BE_EXPORT_VARIABLE be_define_const_native_module(debug);
