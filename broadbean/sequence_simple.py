import logging
import numpy as np
from typing import List, Dict 
from schema import Schema, Or, Optional
from .element import Element


log = logging.getLogger(__name__)

fs_schema = Schema({int: {'type': Or('subsequence', 'element'),
                          'content': {int: {'data': {Or(str, int): {str: np.ndarray}},
                                            Optional('sequencing'): {Optional(str):
                                                                    int}}},
                          'sequencing': {Optional(str): int}}})

class Sequence:
    """
    Sequence object
    thin wrapper around a list
    how is this different from a list?-> has sequencing options
    """

    def __init__(self, elements:List[Element]=[]) -> None:
        self.elements = elements
        # if this is a subsequence
        self.sequencing = {}

    def forge(self, SR, context) -> Dict[int, Dict]:
        output: Dict[int, Dict] = {}
        for ie, elem in enumerate(self.elements):
            item = {}
            item['sequencing'] = elem.sequencing
            item['content'] = {}
            if isinstance(elem, Sequence):
                item['type'] = 'subsequence'
                for ies, subelem in enumerate(elem.elements):
                    item['content'][ise] = {
                        'data': subelem.forge(SR, context),
                        'sequencing': subelem.sequencing}
            elif isinstance(elem, Element):
                item['type'] = 'element'
                item['content'][1] = {'data': elem.forge(SR, context)}
            output[ie] = item
        return output