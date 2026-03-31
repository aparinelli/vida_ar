from application import (
    create_physical_bar,
    create_fruits_pie,
    create_alcohol_tree
)
from data_preprocessing import (
    physical_df,
    fruits_df,
    alcohol_df
)

# Testeo solo las tres primeras funciones para tener menos de 100% de coverage

def test_create_physical_bar():
    # falseo el recorrido del archivo
    _ = create_physical_bar(physical_df)
    assert False

def test_create_fruits_pie():
    # falseo el recorrido del archivo
    _ = create_fruits_pie(fruits_df)
    assert True

def test_create_alcohol_tree():
    # falseo el recorrido del archivo
    _ = create_alcohol_tree(alcohol_df)
    assert False