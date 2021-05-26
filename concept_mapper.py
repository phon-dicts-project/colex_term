import csv
import pyconcepticon.api
from tqdm import tqdm
from pyconcepticon.glosses import concept_map

CON_PATH = 'D:\github repos\concepticon-data'
Concepticon = pyconcepticon.api.Concepticon(CON_PATH)

glots = ['andi1255', 'tind1238', 'ghod1238', 'bagv1239', 'kara1474', 'akhv1239']
for glot in tqdm(glots):
    with open(f'final_data_{glot}.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    lang = 'ru'
    ru_map = Concepticon._get_map_for_language(lang)

    glosses = [entry.get('meaning_ru') for entry in data]
    map_ref = [entry[1] for entry in ru_map]

    mapping = concept_map(glosses, map_ref, language=lang)

    mapped_glosses = {}
    mapped_idxs = {}
    for gloss_idx, gloss in enumerate(glosses):
        match_idxs, _ = mapping.get(gloss_idx, ([], None))

        match_glosses = [
            map_ref[match_idx].split('///')[0]
            for match_idx in match_idxs
        ]
    
        true_match_idxs = [
            ru_map[match_idx][0]
            for match_idx in match_idxs
        ]

        mapped_idxs[gloss_idx + 1] = true_match_idxs
        mapped_glosses[gloss_idx + 1] = match_glosses


    with open(f'final_data_{glot}_mapped.csv', 'w', encoding='utf-8') as mf:
        mf.write('ID,meaning_ru,idxs,glosses,lemma,glottocode,reference\n')

        for row in data:
            idxs = mapped_idxs.get(int(row['ID']), [])
            glosses = mapped_glosses.get(int(row['ID']), [])

            if idxs and glosses:
                buf = [
                    row['ID'],
                    row['meaning_ru'].replace(',', ';'),
                    '|'.join([str(idx) for idx in idxs]),
                    '|'.join(glosses).replace(',', ';'),
                    row['lemma'].replace(',', ''),
                    row['glottocode'],
                    row['reference']
                ]

                mf.write('%s\n' % ','.join(buf))
