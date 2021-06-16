import lxml.etree as et
import os
from os.path import join
import json

fail_counter = 0
total_counter = 0

# input_path = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/additional_files'
input_path = '/Users/vic/Downloads/add-md'
output_path = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/additional_files_json'
error_file = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/additional_files_conversion_error'


def write_dict_to_file(ds_dict, full_output_path):
    with open(full_output_path, 'w') as f:
        json.dump(ds_dict, f)
        f.writelines('\n')


def make_full_output_filename(full_input_file):
    basename = os.path.basename(full_input_file.replace('xml', 'json'))
    return join(output_path, basename)


def get_id(root):
    fields = list()
    id_agency = 'Steinmetz Archive'
    id_nodes = root.xpath('./docDscr/citation/titlStmt/IDNo')
    if id_nodes and isinstance(id_nodes, list):
        for id_node in id_nodes:
            node_dict = dict()
            id_no = id_node.text

            otherIdAgency_dict = dict()
            otherIdAgency_dict['typeName'] = 'otherIdAgency'
            otherIdAgency_dict['multiple'] = False
            otherIdAgency_dict['typeClass'] = 'primitive'
            otherIdAgency_dict['value'] = id_agency

            otherIdValue_dict = dict()
            otherIdValue_dict['typeName'] = 'otherIdValue'
            otherIdValue_dict['multiple'] = False
            otherIdValue_dict['typeClass'] = 'primitive'
            otherIdValue_dict['value'] = f'{id_no}'

            node_dict['otherIdAgency'] = otherIdAgency_dict
            node_dict['otherIdValue'] = otherIdValue_dict

            fields.append(node_dict)

    if len(fields) > 0:
        otherId_dict = dict()
        otherId_dict['typeName'] = 'otherId'
        otherId_dict['multiple'] = False
        otherId_dict['typeClass'] = 'compound'
        otherId_dict['value'] = fields
        return otherId_dict
    raise Exception('cannot find id')


def get_prodPlac():
    fields = list()
    prodPlac = 'Steinmetz Archive, Amsterdam'
    prodPlac_dict = dict()
    prodPlac_dict['typeName'] = 'productionPlace'
    prodPlac_dict['multiple'] = False
    prodPlac_dict['typeClass'] = 'primitive'
    prodPlac_dict['value'] = prodPlac

    fields.append(prodPlac_dict)

    return fields


def get_time_period_covered(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/stdyInfo/sumDscr/timePrd')

    if nodes is not None and isinstance(nodes, list) and len(nodes) > 2:
        start_date = nodes[1].text
        stop_date = nodes[2].text

        node_dict = dict()

        timePeriodCoveredStart_dict = dict()
        timePeriodCoveredStart_dict['typeName'] = 'timePeriodCoveredStart'
        timePeriodCoveredStart_dict['multiple'] = False
        timePeriodCoveredStart_dict['typeClass'] = 'primitive'
        timePeriodCoveredStart_dict['value'] = start_date

        timePeriodCoveredEnd_dict = dict()
        timePeriodCoveredEnd_dict['typeName'] = 'timePeriodCoveredEnd'
        timePeriodCoveredEnd_dict['multiple'] = False
        timePeriodCoveredEnd_dict['typeClass'] = 'primitive'
        timePeriodCoveredEnd_dict['value'] = stop_date

        node_dict['timePeriodCoveredStart'] = timePeriodCoveredStart_dict
        node_dict['timePeriodCoveredEnd'] = timePeriodCoveredEnd_dict

        timePeriodCovered_dict = dict()
        timePeriodCovered_dict["typeName"] = "timePeriodCovered"
        timePeriodCovered_dict["multiple"] = True
        timePeriodCovered_dict["typeClass"] = "compound"
        timePeriodCovered_dict["value"] = [node_dict]

        fields.append(timePeriodCovered_dict)
        return fields
    return None


def get_colldate(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/stdyInfo/sumDscr/collDate')

    if nodes is not None and isinstance(nodes, list) and len(nodes) > 1:
        start_date = nodes[0].text
        stop_date = nodes[1].text

        node_dict = dict()

        dateOfCollectionStart_dict = dict()
        dateOfCollectionStart_dict['typeName'] = 'dateOfCollectionStart'
        dateOfCollectionStart_dict['multiple'] = False
        dateOfCollectionStart_dict['typeClass'] = 'primitive'
        dateOfCollectionStart_dict['value'] = start_date

        dateOfCollectionEnd_dict = dict()
        dateOfCollectionEnd_dict['typeName'] = 'dateOfCollectionEnd'
        dateOfCollectionEnd_dict['multiple'] = False
        dateOfCollectionEnd_dict['typeClass'] = 'primitive'
        dateOfCollectionEnd_dict['value'] = stop_date

        node_dict['dateOfCollectionStart'] = dateOfCollectionStart_dict
        node_dict['dateOfCollectionEnd'] = dateOfCollectionEnd_dict

        dateOfCollection_dict = dict()
        dateOfCollection_dict["typeName"] = "dateOfCollection"
        dateOfCollection_dict["multiple"] = False
        dateOfCollection_dict["typeClass"] = "compound"
        dateOfCollection_dict["value"] = [node_dict]

        fields.append(dateOfCollection_dict)
        return fields
    return None


def get_geocoverage_nation(root):
    fields = list()
    nodes_country = root.xpath('./stdyDescr/stdyInfo/sumDscr/nation')
    nodes_other = root.xpath('./stdyDescr/stdyInfo/sumDscr/geoCover')
    node_dict = dict()

    if nodes_country is not None and isinstance(nodes_country, list) and len(nodes_country) == 1:
        geo_nation = nodes_country[0].text

        geo_nation_dict = dict()
        geo_nation_dict['typeName'] = 'country'
        geo_nation_dict['multiple'] = False
        geo_nation_dict['typeClass'] = 'primitive'
        geo_nation_dict['value'] = geo_nation
        node_dict['country'] = geo_nation_dict

    if nodes_other is not None and isinstance(nodes_other, list) and len(nodes_other) == 1:
        geo_other = nodes_other[0].text

        geo_other_dict = dict()
        geo_other_dict['typeName'] = 'otherGeographicCoverage'
        geo_other_dict['multiple'] = False
        geo_other_dict['typeClass'] = 'primitive'
        geo_other_dict['value'] = geo_other
        node_dict['otherGeographicCoverage'] = geo_other_dict

    if len(node_dict.keys()) > 0:
        geo_dict = dict()
        geo_dict["typeName"] = "geographicCoverage"
        geo_dict["multiple"] = True
        geo_dict["typeClass"] = "compound"
        geo_dict["value"] = [node_dict]

        fields.append(geo_dict)
        return fields
    return None


def get_geounit(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/stdyInfo/sumDscr/geoUnit')

    if nodes and isinstance(nodes, list) and len(nodes) > 0:
        geoUnit_dict = dict()
        geoUnit_dict['typeName'] = 'geographicUnit'
        geoUnit_dict['multiple'] = False
        geoUnit_dict['typeClass'] = 'primitive'
        geoUnit_dict['value'] = [i.text for i in nodes]

        fields.append(geoUnit_dict)

        return fields
    return None


def get_anlyunit(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/stdyInfo/sumDscr/anlyUnit')

    if nodes is not None and isinstance(nodes, list) and len(nodes) > 0:
        terms_list = list()
        for term in nodes:
            term_dict = dict()
            term_dict['typeName'] = 'unitOfAnalysis-term'
            term_dict['multiple'] = False
            term_dict['typeClass'] = 'primitive'
            term_dict['value'] = term.text
            terms_list.append({"unitOfAnalysis-term": term_dict})

        terms_dict = dict()
        terms_dict["typeName"] = "unitOfAnalysis"
        terms_dict["multiple"] = True
        terms_dict["typeClass"] = "compound"
        terms_dict["value"] = terms_list

        fields.append(terms_dict)
        return fields


def get_universe(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/stdyInfo/sumDscr/universe')

    if nodes and isinstance(nodes, list) and len(nodes) > 0:
        universe_dict = dict()
        universe_dict['typeName'] = 'universe'
        universe_dict['multiple'] = True
        universe_dict['typeClass'] = 'primitive'
        universe_dict['value'] = [i.text for i in nodes]

        fields.append(universe_dict)

        return fields
    return None


def get_kindOfData(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/stdyInfo/sumDscr/dataKind')

    if nodes and isinstance(nodes, list) and len(nodes) > 0:
        kindOfData_dict = dict()
        kindOfData_dict['typeName'] = 'kindOfData'
        kindOfData_dict['multiple'] = True
        kindOfData_dict['typeClass'] = 'primitive'
        kindOfData_dict['value'] = [i.text for i in nodes]

        fields.append(kindOfData_dict)

        return fields
    return None


def get_timeMeth(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/method/dataColl/timeMeth')

    if nodes is not None and isinstance(nodes, list) and len(nodes) > 0:
        terms_list = list()
        for term in nodes:
            term_dict = dict()
            term_dict['typeName'] = 'timeMethod-term'
            term_dict['multiple'] = False
            term_dict['typeClass'] = 'primitive'
            term_dict['value'] = term.text
            terms_list.append({"timeMethod-term": term_dict})

        terms_dict = dict()
        terms_dict["typeName"] = "timeMethod"
        terms_dict["multiple"] = True
        terms_dict["typeClass"] = "compound"
        terms_dict["value"] = terms_list

        fields.append(terms_dict)
        return fields


def get_datacollector(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/method/dataColl/datacollector')

    if nodes and isinstance(nodes, list) and len(nodes) > 0:
        datacollector_dict = dict()
        datacollector_dict['typeName'] = 'dataCollector'
        datacollector_dict['multiple'] = False
        datacollector_dict['typeClass'] = 'primitive'
        datacollector_dict['value'] = nodes[0].text

        fields.append(datacollector_dict)

        return fields
    return None


def get_frequenc(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/method/dataColl/frequenc')

    if nodes and isinstance(nodes, list) and len(nodes) > 0:
        datacollector_dict = dict()
        datacollector_dict['typeName'] = 'frequencyOfDataCollection'
        datacollector_dict['multiple'] = False
        datacollector_dict['typeClass'] = 'primitive'
        datacollector_dict['value'] = nodes[0].text

        fields.append(datacollector_dict)

        return fields
    return None


def get_sampProc(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/method/dataColl/sampProc')

    if nodes and isinstance(nodes, list) and len(nodes) > 0:
        sampProc_dict = dict()
        sampProc_dict['typeName'] = 'samplingProcedure'
        sampProc_dict['multiple'] = False
        sampProc_dict['typeClass'] = 'primitive'
        sampProc_dict['value'] = [i.text for i in nodes]

        fields.append(sampProc_dict)

        return fields
    return None


def get_collMode(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/method/dataColl/collMode')

    if nodes is not None and isinstance(nodes, list) and len(nodes) > 0:
        terms_list = list()
        for term in nodes:
            term_dict = dict()
            term_dict['typeName'] = 'collectionMode-term'
            term_dict['multiple'] = False
            term_dict['typeClass'] = 'primitive'
            term_dict['value'] = term.text
            terms_list.append({"collectionMode-term": term_dict})

        terms_dict = dict()
        terms_dict["typeName"] = "collectionMode"
        terms_dict["multiple"] = False
        terms_dict["typeClass"] = "compound"
        terms_dict["value"] = terms_list

        fields.append(terms_dict)
        return fields


def get_resInstru(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/method/dataColl/resInstru')

    if nodes is not None and isinstance(nodes, list) and len(nodes) > 0:
        terms_list = list()
        for term in nodes:
            term_dict = dict()
            term_dict['typeName'] = 'researchInstrument-term'
            term_dict['multiple'] = False
            term_dict['typeClass'] = 'primitive'
            term_dict['value'] = term.text
            terms_list.append({"researchInstrument-term": term_dict})

        terms_dict = dict()
        terms_dict["typeName"] = "researchInstrument"
        terms_dict["multiple"] = False
        terms_dict["typeClass"] = "compound"
        terms_dict["value"] = terms_list

        fields.append(terms_dict)
        return fields


def get_collSitu(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/method/dataColl/collSitu')

    if nodes and isinstance(nodes, list) and len(nodes) > 0:
        collSitu_dict = dict()
        collSitu_dict['typeName'] = 'dataCollectionSituation'
        collSitu_dict['multiple'] = False
        collSitu_dict['typeClass'] = 'primitive'
        collSitu_dict['value'] = nodes[0].text

        fields.append(collSitu_dict)

        return fields
    return None


def get_actMin(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/method/dataColl/actMin')

    if nodes and isinstance(nodes, list) and len(nodes) > 0:
        actMin_dict = dict()
        actMin_dict['typeName'] = 'actionsToMinimizeLoss'
        actMin_dict['multiple'] = False
        actMin_dict['typeClass'] = 'primitive'
        actMin_dict['value'] = nodes[0].text

        fields.append(actMin_dict)

        return fields
    return None


def get_weight(root):
    fields = list()
    nodes = root.xpath('./stdyDescr/method/dataColl/weight')

    if nodes and isinstance(nodes, list) and len(nodes) > 0:
        weight_dict = dict()
        weight_dict['typeName'] = 'weighting'
        weight_dict['multiple'] = False
        weight_dict['typeClass'] = 'primitive'
        weight_dict['value'] = nodes[0].text

        fields.append(weight_dict)

        return fields
    return None


def convert_xml_to_dict(full_input_file):
    dom = et.parse(full_input_file)
    root = dom.getroot()

    # create list which contains all the fields
    fields = list()

    # get id number and agency
    fields.append(get_id(root))

    # get production place
    # TODO: enable when finished
    fields.extend(get_prodPlac())

    # get time period covered
    time_period_covered = get_time_period_covered(root)
    if time_period_covered is not None:
        fields.extend(time_period_covered)

    # get collect date
    colldata = get_colldate(root)
    if colldata is not None:
        fields.extend(colldata)

    # get nation and other geo coverage
    geocoverage_nation = get_geocoverage_nation(root)
    if geocoverage_nation is not None:
        fields.extend(geocoverage_nation)

    # get geo unit
    geounit = get_geounit(root)
    if geounit is not None:
        fields.extend(geounit)

    # get unit of analysis
    anlyunit = get_anlyunit(root)
    if anlyunit is not None:
        fields.extend(anlyunit)

    # get universe
    universe = get_universe(root)
    if universe is not None:
        fields.extend(universe)

    # get kindOfData
    kindOfData = get_kindOfData(root)
    if kindOfData is not None:
        fields.extend(kindOfData)

    # get timeMeth
    timeMeth = get_timeMeth(root)
    if timeMeth is not None:
        fields.extend(timeMeth)

    # get datacollector
    # TODO: enable when finished
    datacollector = get_datacollector(root)
    if datacollector is not None:
        fields.extend(datacollector)

    # get frequenc
    # TODO: enable when finished
    frenquenc = get_frequenc(root)
    if frenquenc is not None:
        fields.extend(frenquenc)

    # get sampProc
    sampProc = get_sampProc(root)
    if sampProc is not None:
        fields.extend(sampProc)

    # get collMode
    # TODO: collMode is a single valued CV field which causes problems when editMetadata. See notes please
    #
    # collMode = get_collMode(root)
    # if collMode is not None:
    #     fields.extend(collMode)

    # get resInstru
    # TODO: resInstru is a single valued CV field which causes problems when editMetadata. See notes please
    #
    # resInstru = get_resInstru(root)
    # if resInstru is not None:
    #     fields.extend(resInstru)

    # get collSitu
    # TODO: enable when finished
    collSitu = get_collSitu(root)
    if collSitu is not None:
        fields.extend(collSitu)

    # get actMin
    # TODO: enable when finished
    actMin = get_actMin(root)
    if actMin is not None:
        fields.extend(actMin)

    # get weight
    # TODO: enable when finished
    weight = get_weight(root)
    if weight is not None:
        fields.extend(weight)

    # return json.dumps({'fields': fields}, indent=2)
    return {'fields': fields}


def __main__():
    global total_counter, fail_counter
    for root, dirs, files in os.walk(input_path):
        for name in files:
            full_input_file = join(root, name)
            print(f'### {total_counter} converting {full_input_file}')
            full_output_file = make_full_output_filename(full_input_file)
            ds_dict = convert_xml_to_dict(full_input_file)
            write_dict_to_file(ds_dict, full_output_file)
            print(f'### {total_counter} done with {full_input_file}')
            total_counter += 1

    print(f'In total {total_counter} files processed, and {fail_counter} failed; Please see the log {error_file} for errors')


if __name__ == '__main__':
    __main__()
