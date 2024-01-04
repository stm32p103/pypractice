import re
from openpyxl.utils.cell import get_column_letter

_pattern = r"R((\[(?P<rel_row>[0-9]+)\])|(?P<abs_row>[0-9]+))?C((\[(?P<rel_col>[0-9]+)\])|(?P<abs_col>[0-9]+))?"

def _rc2a1( matchobj, baseRow: int, baseCol: int ):
    # 行の変換
    if matchobj[ 'abs_row' ] != None:
        row = int( matchobj[ 'abs_row' ] )    
    elif matchobj[ 'rel_row' ] != None:
        row = baseRow + int( matchobj[ 'rel_row' ] )
    else:
        row = baseRow

    # 列の変換   
    if matchobj[ 'abs_col' ] != None:
        col = int( matchobj[ 'abs_col' ] )    
    elif matchobj[ 'rel_col' ] != None:
        col = baseCol + int( matchobj[ 'rel_col' ] )
    else:
        col = baseCol

    if row <= 0 or col <= 0:
        raise ValueError( f'row={row}, col={col}' )

    # A1形式で返す
    coord = get_column_letter( col ) + str( row )
    return coord


def convert_rc2a1( formula: str | None, baseRow: int, baseCol: int ) -> str | None:
    '''
    Matchに含まれる名前付きグループの値から、数式に含まれるR1C1形式のセル参照をA1形式に変換する。

    * 相対参照の場合は`baseRow`と`baseCol`を基準に行・列を算出する。
    * `=`から始まる数式でなければ変換しない。
    '''

    # = から始まらない場合はそのまま返す
    if ( formula == None ) or ( len( formula ) == 0 ) or ( formula[0] != '=' ):
        return formula

    def conv( matchobj ):
        return _rc2a1( matchobj, baseRow, baseCol )

    return re.sub( _pattern, conv, formula )