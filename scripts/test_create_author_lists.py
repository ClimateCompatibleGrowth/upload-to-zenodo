from create_author_lists import get_authors
import pandas as pd

def test_get_authors():

    contributors = [1]
    data = pd.DataFrame(
        data=[[1, 'Joe', 'Bloggs', '0000-0000-0000-0001', 'KTH']],
        columns=['id', 'firstname', 'lastname', 'orcid', 'institution']
    ).set_index('id')

    data['lookup'] = data['firstname'] + " " + data['lastname']

    actual = get_authors(contributors, data)
    expected = [{
                "name": 'Bloggs, Joe',
                "affiliation": 'KTH',
                "orcid":  '0000-0000-0000-0001'
            }]
    assert actual == expected