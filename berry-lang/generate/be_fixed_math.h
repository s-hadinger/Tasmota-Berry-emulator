#include "be_constobj.h"

static be_define_const_map_slots(m_libmath_map) {
    { be_ckey(deg, 20), be_ckv_func(m_deg) },
    { be_ckey(imin, 11), be_ckv_int(M_IMIN) },
    { be_ckey(rad, -1), be_ckv_func(m_rad) },
    { be_ckey(cosh, -1), be_ckv_func(m_cosh) },
    { be_ckey(abs, -1), be_ckv_func(m_abs) },
    { be_ckey(exp, 2), be_ckv_func(m_exp) },
    { be_ckey(asin, -1), be_ckv_func(m_asin) },
    { be_ckey(log10, -1), be_ckv_func(m_log10) },
    { be_ckey(inf, 19), be_ckv_real(INFINITY) },
    { be_ckey(srand, -1), be_ckv_func(m_srand) },
    { be_ckey(isnan, -1), be_ckv_func(m_isnan) },
    { be_ckey(isinf, -1), be_ckv_func(m_isinf) },
    { be_ckey(atan2, -1), be_ckv_func(m_atan2) },
    { be_ckey(sin, -1), be_ckv_func(m_sin) },
    { be_ckey(imax, -1), be_ckv_int(M_IMAX) },
    { be_ckey(sqrt, -1), be_ckv_func(m_sqrt) },
    { be_ckey(tanh, 7), be_ckv_func(m_tanh) },
    { be_ckey(log, -1), be_ckv_func(m_log) },
    { be_ckey(pi, 14), be_ckv_real(M_PI) },
    { be_ckey(ceil, 5), be_ckv_func(m_ceil) },
    { be_ckey(acos, 30), be_ckv_func(m_acos) },
    { be_ckey(pow, -1), be_ckv_func(m_pow) },
    { be_ckey(rand, -1), be_ckv_func(m_rand) },
    { be_ckey(min, 12), be_ckv_func(m_min) },
    { be_ckey(tan, 1), be_ckv_func(m_tan) },
    { be_ckey(max, -1), be_ckv_func(m_max) },
    { be_ckey(nan, -1), be_ckv_real(NAN) },
    { be_ckey(round, 4), be_ckv_func(m_round) },
    { be_ckey(cos, 3), be_ckv_func(m_cos) },
    { be_ckey(floor, -1), be_ckv_func(m_floor) },
    { be_ckey(sinh, -1), be_ckv_func(m_sinh) },
    { be_ckey(atan, 0), be_ckv_func(m_atan) },
};

static be_define_const_map(
    m_libmath_map,
    32
);

static be_define_const_module(
    m_libmath,
    "math"
);

BE_EXPORT_VARIABLE be_define_const_native_module(math);
