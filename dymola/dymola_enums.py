# Copyright (c) 2013-2017 Dassault Systemes. All rights reserved.

def __enum(**enums):
    # pylint: disable=missing-docstring
    return type("Enum", (), enums)

LinePattern = __enum(none=1, Solid=2, Dash=3, Dot=4, DashDot=5, DashDotDot=6)
"""
This corresponds to the Dymola/Modelica enumeration with the same name.

:Members:
 * none - 1
 * Solid - 2
 * Dash - 3
 * Dot - 4
 * DashDot - 5
 * DashDotDot - 6
"""

MarkerStyle = __enum(none=1, Cross=2, Circle=3, Square=4, FilledCircle=5, FilledSquare=6, TriangleDown=7, TriangleUp=8, Diamond=9, Dot=10, SmallSquare=11, Point=12)
"""
This corresponds to the Dymola/Modelica enumeration with the same name.

:Members:
 * none - 1
 * Cross - 2
 * Circle - 3
 * Square - 4
 * FilledCircle - 5
 * FilledSquare - 6
 * TriangleDown - 7
 * TriangleUp - 8
 * Diamond - 9
 * Dot - 10
 * SmallSquare - 11
 * Point - 12
"""

TextStyle = __enum(Bold=1, Italic=2, UnderLine=3)
"""
This corresponds to the Dymola/Modelica enumeration with the same name.

:Members:
 * Bold - 1
 * Italic - 2
 * UnderLine - 3
"""

TextAlignment = __enum(Left=1, Center=2, Right=3)
"""
This corresponds to the Dymola/Modelica enumeration with the same name.

:Members:
 * Left - 1
 * Center - 2
 * Right - 3
"""

SignalOperator = __enum(Min=1, Max=2, ArithmeticMean=3, RectifiedMean=4, RMS=5, ACCoupledRMS=6, SlewRate=7, THD=8, FirstHarmonic=9)
"""
This corresponds to the Dymola/Modelica enumeration with the same name.

:Members:
 * Min - 1
 * Max - 2
 * ArithmeticMean - 3
 * RectifiedMean - 4
 * RMS - 5
 * ACCoupledRMS - 6
 * SlewRate - 7
 * THD - 8
 * FirstHarmonic - 9
"""

