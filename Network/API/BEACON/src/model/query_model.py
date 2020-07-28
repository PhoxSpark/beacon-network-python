"""query_model
Disabled some lintings on some lines justified, necessary violation of those
informative lintings that are too strict. Also, disabled on a for with
unused variable just because of the laziness of use a normal while loop.

:return: [description]
:rtype: [type]
"""

import logging as log
from ..controller.dao import AccesDataBase
from ..blueprint.info import get_database_access
from ..blueprint.info import get_beacon_info
from ... import BEACON_CONFIG_FILE

REFERENCE_NAMES = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19",
    "20", "21", "22", "X", "Y", "MT"
]
REFERENCE_BASES = ["A", "C", "G", "T", "N"]

class QueryModel():                                                                                 # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """Object to build the full response from the database.
    Attribute "response" will have the JSON to show to the user.
    """
    def __init__(self, params):
        """Initialize and fill dictionaries.

        :param params: Parameters for the API
        :type params: dict()
        """

        self.dataset_response = list()
        self.result = dict()
        self.query_response = dict()
        self.response = dict()
        self.missed_results = dict()

        self.http_code = 200
        self.params = params
        self.abort = False

        self.exists = False
        self.error = None

        self.beacon_info, self.http_code = get_beacon_info(
            conf_file=BEACON_CONFIG_FILE,
            include_datasets=False
        )

        if self.http_code != 503:
            self.__make_query()
            self.__filter_dictionary()
            self.__dataset_response_builder()
            self.__check_if_exists()
        self.__build_error()
        self.__build_response()


    def __make_query(self):
        """Make a connection
        Make a new connection saving the data on a dictionary. It will filter
        the assemblyID and the dataset ID.
        """
        tmp_dao = AccesDataBase()
        dataset_with_aid = dict()
        query_sql = str()

        #Getting assemblyId datasets
        if self.params["assemblyId"] is None:
            log.error("Assembly ID not specified.")
            self.abort = True
            self.http_code = 400
        try:
            query_sql = "SELECT * " + \
                        "FROM beacon_dataset_table " + \
                        "WHERE reference_genome = '" + self.params["assemblyId"] + "';"
            tmp_dao.connect(get_database_access("beacon/database.ini"))
            tmp_dao.complex_select_data(query_sql)
            dataset_with_aid = tmp_dao.response
        except TypeError:
            log.error("AssemblyID not specified.")
            self.abort = True
            self.http_code = 400

        #Filtering datasets id
        if self.params["datasetIds"] is None:
            for dataset in dataset_with_aid:
                query_sql = "SELECT * " + \
                            "FROM beacon_data_table"
                tmp_dao.complex_select_data(query_sql)
                self.query_response[dataset["stable_id"]] = tmp_dao.response
        else:
            for dataset in dataset_with_aid:
                query_sql = "SELECT * " + \
                             "FROM beacon_data_table " + \
                             "WHERE dataset_id = " + str(dataset["id"]) + ";"
                tmp_dao.complex_select_data(query_sql)
                self.query_response[dataset["stable_id"]] = tmp_dao.response

        if len(self.query_response) == 0:
            log.error("Empty query response!")
            self.abort = True
            self.http_code = 503

        tmp_dao.disconnect()

    def __filter_dictionary(self):                                                                  # pylint: disable=too-many-branches
        """Apply filters
        Modify the obtained dictionary from the database applying
        the filters specified by the user. There are some mandatory
        filters but the majority are optional. I marked the mandatory
        with '*'.
        """
        if not self.abort:
            log.debug("Iterating trough datasets.")
            for dataset in self.query_response:
                self.result[dataset] = list()
                self.missed_results[dataset] = list()
                log.debug("Dataset: %s", dataset)
                ### Reference name (chromosome)* ###
                for data in self.query_response[dataset]:
                    if self.params["referenceName"] in REFERENCE_NAMES \
                    and not self.abort:
                        if data["chromosome"] == self.params["referenceName"]:
                            self.result[dataset].append(data)
                        else:
                            self.missed_results[dataset].append(data)
                    else:
                        log.error("Reference name %s is not valid.", self.params["referenceName"])
                        self.abort = True
                        self.http_code = 400
                ### Reference name (chromosome)* ###

                ### ReferenceBases* ###
                #Check if input is valid
                if self.params["referenceBases"] is None:
                    self.params["referenceBases"] = "O"
                for character in self.params["referenceBases"]:
                    if character not in REFERENCE_BASES:
                        log.error("Reference base not correct.")
                        self.abort = True
                        self.http_code = 400
                #Filter result
                if not self.abort:
                    self.__dict_filter_bases(
                        self.params["referenceBases"],
                        "reference"
                    )

                ### Start and End ###
                #You can use all of them separately but range with single
                #will be pretty much useless.
                if not self.abort:
                    if self.params["start"] is not None:
                        print(self.result)
                        self.__dict_filter(
                            self.params["start"],
                            "start"
                        )
                    if self.params["end"] is not None:
                        self.__dict_filter(
                            self.params["end"],
                            "end"
                        )
                    if self.params["startMin"] is not None \
                    and self.params["startMax"] is not None:
                        self.__dict_filer_range(
                            self.params["startMin"],
                            self.params["startMax"],
                            "start"
                        )
                    if self.params["endMin"] is not None \
                    and self.params["endMax"] is not None:
                        self.__dict_filer_range(
                            self.params["endMin"],
                            self.params["endMax"],
                            "end"
                        )

                ### AlternateBases ###
                if not self.abort and self.params["alternateBases"] is not None:
                    self.__dict_filter_bases(
                        self.params["alternateBases"],
                        "alternate"
                    )

                ### VariantType ###
                if not self.abort and self.params["variantType"] is not None:
                    self.__dict_filter(
                        self.params["variantType"],
                        "type"
                    )

                ### MateName ###
                if not self.abort and self.params["mateName"] is not None:
                    self.__dict_filter(
                        self.params["mateName"],
                        "chromosome"
                    )

        else:
            log.warning("Query aborted.")

    def __check_if_exists(self):
        """Check if the query was successful
        If the query maded exists in the database it will set the attribute
        exists to true.
        """
        tmp_counter = 0
        for dataset in self.result:
            for data in self.result[dataset]:                                                       # pylint: disable=unused-variable
                tmp_counter = tmp_counter + 1
        if tmp_counter > 0:
            self.exists = True

    def __build_error(self):
        """Error dictionary
        Build the error dictionary from the HTTP code and the abort
        attribute.
        """
        tmp_message = "No additional information."

        if self.abort:
            if self.http_code == 400:
                tmp_message = "Bad request."
            if self.http_code == 401:
                tmp_message = "Unauthorised."
            if self.http_code == 403:
                tmp_message = "Forbidden."
            if self.http_code == 503:
                tmp_message = "Service unavailable. May the Database didn't answer?"

            self.error = {
                "errorCode"     : self.http_code,
                "errorMessage"  : tmp_message
            }

    def __build_response(self):
        """Build the JSON response
        It will append the datasetAlleleResponses (if specified) and the
        error if there's any.
        """
        self.response = {
            "beaconId"                  : self.beacon_info["id"],
            "apiVersion"                : self.beacon_info["apiVersion"],
            "exists"                    : self.exists,
            "alleleRequest"             : self.params,
            "datasetAlleleResponses"    : self.dataset_response,
            "error"                     : self.error,
            "info"                      : None,
            "beaconHandover"            : None
        }

    def __dataset_response_builder(self):
        """Build dataset response
        Build the dictionary for the dataset response to inject it into
        the JSON response.
        """
        tmp_show = False
        tmp_datasets = None

        #Reading param responses
        if self.params["includeDatasetResponses"] == "ALL":
            #Show all responses without filter
            tmp_datasets = self.query_response
            tmp_show = True
        elif self.params["includeDatasetResponses"] == "HIT":
            #Show good responses
            tmp_datasets = self.result
            tmp_show = True
        elif self.params["includeDatasetResponses"] == "MISS":
            #Show bad responses
            tmp_datasets = self.missed_results
            tmp_show = True
        else:
            self.dataset_response = None

        #Iteration for each dataset
        if tmp_show:
            for dataset in tmp_datasets:
                for row in tmp_datasets[dataset]:

                    tmp_counter = len(self.result[dataset])
                    tmp_current_exist = True

                    if row in self.missed_results[dataset]:
                        tmp_current_exist = False

                    self.dataset_response.append({
                        "datasetId"          : dataset,
                        "exists"             : tmp_current_exist,
                        "error"              : self.error,
                        "frequency"          : str(row["frequency"]),
                        "variantCount"       : tmp_counter,
                        "callCount"          : row["call_cnt"],
                        "sampleCount"        : row["sample_cnt"],
                        "note"               : None,
                        "externalUrl"        : None,
                        "info"               : None,
                        "datasetHandover"    : None
                    })

    def __dict_filer_range(self, param1, param2, column):
        """Range filter
        It will take values inside a range on a specified column.

        :param param1: Value 1 for the range.
        :type param1: int()
        :param param2: Value 2 for the range.
        :type param2: int()
        :param column: Column to apply the range.
        :type column: str()
        """
        tmp_dict_build = dict()
        tmp_missed = dict()
        #tmp_param = None

        if int(param1) > int(param2): #Int for redundancy
            tmp_param = param2
            param2 = param1
            param1 = tmp_param

        for dataset in self.result:           #Get all the datasets on current dict
            tmp_dict_build[dataset] = list()
            tmp_missed[dataset] = list()
            for data in self.result[dataset]: #Iterate every object on the dataset
                #Comparison with integers because range has to be integer.
                if int(data[column]) >= int(param1) \
                and int(data[column]) <= int(param2):      #Apply filter
                    tmp_dict_build[dataset].append(data)
                else:
                    tmp_missed[dataset].append(data)

        self.result = tmp_dict_build
        self.missed_results = tmp_missed

    def __dict_filter(self, param, column):
        """Filter values on database
        Take a value on the database and check if it's the same than param.

        :param param: Value to check.
        :type param: any
        :param column: Column to apply the filter.
        :type column: str()
        """
        tmp_dict_build = dict()
        tmp_missed = dict()

        for dataset in self.result:           #Get all the datasets on current dict
            tmp_dict_build[dataset] = list()
            tmp_missed[dataset] = list()
            for data in self.result[dataset]: #Iterate every object on the dataset
                #Comparison between string to maximize compatibility
                if str(data[column]) == str(param):      #Apply filter
                    tmp_dict_build[dataset].append(data)
                else:
                    tmp_missed[dataset].append(data)

        self.result = tmp_dict_build
        self.missed_results = tmp_missed


    def __dict_filter_bases(self, param, column):
        """Filter values on database with N as wildcard.
        Same as the normal filter but letting always pass the N character.

        :param param: Value to check.
        :type param: str()
        :param column: Column to apply the filter.
        :type column: str()
        """
        tmp_dict_build = dict()
        tmp_missed = dict()

        for dataset in self.result:           #Get all the datasets on current dict
            tmp_dict_build[dataset] = list()
            tmp_missed[dataset] = list()
            for data in self.result[dataset]: #Iterate every object on the dataset
                #Comparison between string to maximize compatibility
                if str(data[column]) == str(param):        #Apply filter
                    tmp_dict_build[dataset].append(data)
                elif str(param) == "N":
                    tmp_dict_build[dataset].append(data)
                else:
                    tmp_missed[dataset].append(data)

        self.result = tmp_dict_build
        self.missed_results = tmp_missed
