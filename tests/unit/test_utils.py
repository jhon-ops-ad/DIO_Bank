import pytest
from src.controllers.utils import eleva_quadrado, requires_roles
from typing import Literal
from http import HTTPStatus

'''
Tanto o arquivo que é para teste deve começar com 'test_',
como o método também.
'''
@pytest.mark.parametrize("test_input,expected", [(2, 4), (10, 100), (3, 9)])
def test_eleva_quadrado_sucesso(test_input: Literal[2] | Literal[10] | Literal[3], expected: Literal[4] | Literal[100] | Literal[9]):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected


@pytest.mark.parametrize("test_input,exc_class,msg", [
    ('a', TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"), 
    (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'")
])
def test_eleva_quadrado_falha(test_input, exc_class, msg):
    # resultado = eleva_quadrado('a')
    # assert resultado == 'aa'
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)
    assert str(exc.value) == msg


def test_requires_role_success(mocker):
    #Given, o que eu forneço para o teste
    mock_user = mocker.Mock()
    mock_user.role.name = 'admin'

    mocker.patch('src.controllers.utils.get_jwt_identity') 
    mocker.patch('src.controllers.utils.db.get_or_404', return_value=mock_user)

    decorated_function = requires_roles('admin')(lambda: 'success') #lambda se tornou uma função anônima para retornar apenas
    
    #When, é o que executa
    result = decorated_function()#cria um decorador que tem a função anônima que está dentro do requires role
    
    #Then, é o que verifica
    assert result == 'success'


def test_requires_role_fail(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = 'local'

    mocker.patch('src.controllers.utils.get_jwt_identity') 
    mocker.patch('src.controllers.utils.db.get_or_404', return_value=mock_user)

    decorated_function = requires_roles('admin')(lambda: 'success')
    result = decorated_function()

    assert result == ({"message": "User dont have access!"}, HTTPStatus.FORBIDDEN)


