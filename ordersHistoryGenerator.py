import logging
from constants import *
import sys
from math import fmod
from datetime import datetime, timedelta

logger = logging.getLogger(LOGGER_NAME)

# pseudorandomnumbers between 0 and m-1
def lcg(seed=123456789, a=LCG_A, c=LCG_C, m=LCG_M, count=0):
    pseudorandom_numbers = []
    for _ in range(count):
        seed = int(fmod(seed * a + c, m))
        pseudorandom_numbers.append(seed)

    return pseudorandom_numbers


# numbers between 0 and 1, [0, 1)
def pseudorandomNumbersConvert(numbers=[], m=LCG_M):
    new_numbers = []
    for number in numbers:
        new_number = number / m
        new_numbers.append(new_number)

    return new_numbers


# pseudorandom numbers between 0 and 1, [0, 1)
def pseudorandomList(seed=123456789, a=LCG_A, c=LCG_C, m=LCG_M, count=0):
    pseudorandom_numbers = lcg(
        seed=seed,
        a=a,
        c=c,
        m=m,
        count=count,
    )

    pseudorandom_numbers_from_0_to_1 = pseudorandomNumbersConvert(
        pseudorandom_numbers, m
    )

    return pseudorandom_numbers_from_0_to_1


# random_numbers is a list with float: [0, 1)
# return values in range [a, b)
def uniformDistributionRandomList(random_numbers=[], a=0, b=0):
    resultList = []
    # b += 1
    for random_number in random_numbers:

        # [a, b) => b = b + 1
        random_number = int((b - a) * random_number + a)
        resultList.append(random_number)

    return resultList


def getValuesBasedOnIndexes(indexes=[], values=[]):
    resultList = []
    for index in indexes:
        try:
            resultList.append(values[index])
        except Exception as exc:
            logger.error(exc)
            sys.exit()

    return resultList


def sumUpPriceFill(px_InitList, digits_in_price, price_variation_unitsList):
    px_FillList = []

    for index in range(len(px_InitList)):
        price_integer_str = str(int(px_InitList[index]))
        digits_number_int_price = len(price_integer_str)
        digits_after_delimiter = digits_in_price - digits_number_int_price
        precision = 10 ** digits_after_delimiter
        priceVariation = price_variation_unitsList[index] / precision

        px_FillRaw = px_InitList[index] + priceVariation

        px_Fill = format(px_FillRaw, ".%sf" % digits_after_delimiter)

        px_FillList.append(px_Fill)

    return px_FillList


def getRandomNumbersDatetime(seed, count, incrementer, number_datetime_values_order):
    # pseudorandom numbers arrays with values between 0 and 1,
    random_numbers = [[] for _ in range(count)]

    for _ in range(number_datetime_values_order):

        pseudorandom_numbers_from_0_to_1 = pseudorandomList(
            seed=seed,
            a=LCG_A,
            c=LCG_C,
            m=LCG_M,
            count=count,
        )
        seed += incrementer

        for index in range(count):
            random_numbers[index].append(pseudorandom_numbers_from_0_to_1[index])

    return random_numbers, incrementer


# 1 1 1 2 2 2 ... 1 1 1 1 2 2 2 2 ... 1 1 1 2 2 2 <- example of result
def repeatRecordsValues(config, valuesList):
    resultList = []
    index = 0
    for order_type in config["OrdersParameters"]["orders"]:
        for order_number in range(order_type["count"]):

            order_repeats_values = [valuesList[index]] * len(order_type["Statuses"])

            resultList.extend(order_repeats_values)

            index += 1

    return resultList


def repeatRecordsValuesBasedOnStatus(
    config, valuesList, defaultValuesList, statusList, isPrice=False
):
    resultList = []
    # index = 0
    value_index = 0
    temp = 0
    for order_type in config["OrdersParameters"]["orders"]:
        statuses_count = len(order_type["Statuses"])
        for order_number in range(order_type["count"]):
            for index in range(statuses_count):
                last_value = 0
                changed_value = valuesList[value_index]
                default_value = defaultValuesList[value_index]
                if isPrice:
                    default_value = changed_value
                if statuses_count == 1:
                    last_value = default_value
                elif len(resultList) != 0:
                    last_value = resultList[-1]

                status = statusList[temp]
                value_to_append = getValueBasedOnStatus(
                    config["DependentParameters"],
                    last_value,
                    default_value,
                    changed_value,
                    status,
                )
                resultList.append(value_to_append)
                temp += 1
            value_index += 1
        # print(order_number * statuses_count)
        # index += 1
        # print(value_index)
    return resultList


def getValueBasedOnStatus(
    dependenciesParameters, last_value, default_value, changed_value, status
):
    result = 0
    if dependenciesParameters[status] == FILL_WITH_DEFAULT:
        result = default_value
    elif dependenciesParameters[status] == FILL_WITH_ZERO:
        result = 0
    elif dependenciesParameters[status] == FILL_FROM_LAST:
        result = last_value
        # print(last_value, default_value, changed_value, status, result)
    elif dependenciesParameters[status] == FILL_WITH_CHANGED:
        result = changed_value
    else:
        logger.warning("Unexpected status. Check constants and DependentParameters")
    return result


def idGenerator(config):
    pseudorandom_numbers = lcg(
        seed=config["Seeds"]["ID"],
        a=LCG_A,
        c=LCG_C,
        m=LCG_M,
        count=config["OrdersParameters"]["total"],
    )

    idList = []
    for number in pseudorandom_numbers:
        id = "{0:0{1}X}".format(number, 10)
        idList.append(id)

    logger.info("Generated ID")

    return idList


def sideGenerator(config):
    pseudorandom_numbers_from_0_to_1 = pseudorandomList(
        seed=config["Seeds"]["Side"],
        a=LCG_A,
        c=LCG_C,
        m=LCG_M,
        count=config["OrdersParameters"]["total"],
    )

    sideIndexList = uniformDistributionRandomList(
        pseudorandom_numbers_from_0_to_1, a=0, b=len(config["Data"]["Side"])
    )

    sideList = getValuesBasedOnIndexes(sideIndexList, config["Data"]["Side"])

    logger.info("Generated side")

    return sideList


def instrumentGenerator(config):
    pseudorandom_numbers_from_0_to_1 = pseudorandomList(
        seed=config["Seeds"]["Instrument"],
        a=LCG_A,
        c=LCG_C,
        m=LCG_M,
        count=config["OrdersParameters"]["total"],
    )

    instrumentIndexList = uniformDistributionRandomList(
        pseudorandom_numbers_from_0_to_1, a=0, b=len(config["Data"]["Instrument"])
    )

    instrumentList = getValuesBasedOnIndexes(
        instrumentIndexList, config["Data"]["Instrument"]
    )

    logger.info("Generated instrument")

    return instrumentList, instrumentIndexList


def px_InitGenerator(config, instrumentIndexList):
    px_InitRawList = getValuesBasedOnIndexes(
        instrumentIndexList, config["Data"]["Px_Init"]
    )

    px_InitList = []

    for index in range(len(px_InitRawList)):

        price_integer_str = str(int(px_InitRawList[index]))
        digits_number_int_price = len(price_integer_str)
        digits_after_delimiter = (
            config["Parameters"]["digitsInPrice"] - digits_number_int_price
        )

        px_Init = "{0:.{1}f}".format(px_InitRawList[index], digits_after_delimiter)

        px_InitList.append(px_Init)

    logger.info("Generated px_Init")

    return px_InitList, px_InitRawList


def px_FillGenerator(config, px_InitList):
    pseudorandom_numbers_from_0_to_1 = pseudorandomList(
        seed=config["Seeds"]["Px_Fill"],
        a=LCG_A,
        c=LCG_C,
        m=LCG_M,
        count=len(px_InitList),
    )

    # final variation of price in units
    price_variation_unitsList = uniformDistributionRandomList(
        pseudorandom_numbers_from_0_to_1,
        a=-config["Parameters"]["variationUnits"],
        b=config["Parameters"]["variationUnits"],
    )

    px_FillList = sumUpPriceFill(
        px_InitList, config["Parameters"]["digitsInPrice"], price_variation_unitsList
    )

    logger.info("Generated px_Fill")

    return px_FillList


def volume_InitGenerator(config):
    pseudorandom_numbers_from_0_to_1 = pseudorandomList(
        seed=config["Seeds"]["Volume_Init"],
        a=LCG_A,
        c=LCG_C,
        m=LCG_M,
        count=config["OrdersParameters"]["total"],
    )

    volume_InitRawList = uniformDistributionRandomList(
        pseudorandom_numbers_from_0_to_1,
        a=config["Parameters"]["minVolume"],
        b=config["Parameters"]["maxVolume"],
    )

    volume_InitList = []

    for volume_InitRaw in volume_InitRawList:
        volume_Init = round(volume_InitRaw, -3)
        volume_InitList.append(volume_Init)

    logger.info("Generated volume_Init")

    return volume_InitList


def volume_FillGenerator(config, volume_InitList):
    pseudorandom_numbers_from_0_to_1 = pseudorandomList(
        seed=config["Seeds"]["Volume_Fill"],
        a=LCG_A,
        c=LCG_C,
        m=LCG_M,
        count=config["OrdersParameters"]["total"],
    )

    volume_FillRawList = []

    for index in range(len(pseudorandom_numbers_from_0_to_1)):
        b = volume_InitList[index]
        a = config["Parameters"]["minVolume"]
        random = pseudorandom_numbers_from_0_to_1[index]
        # (b - a) * random + a => x is in [a, b)
        volume_FillRaw = int((b - a) * random + a)
        volume_FillRawList.append(volume_FillRaw)

    volume_FillList = []
    index = 0
    for volume_FillRaw in volume_FillRawList:
        # print(volume_FillRaw)
        volume_Fill = (volume_FillRaw // 1000) * 1000
        # if volume_Fill == volume_InitList[index] :
        #     print("asdf")
        volume_FillList.append(volume_Fill)
        index += 1

    logger.info("Generated volume_Fill")

    return volume_FillList


def notesGenerator(config):
    pseudorandom_numbers_from_0_to_1 = pseudorandomList(
        seed=config["Seeds"]["Notes"],
        a=LCG_A,
        c=LCG_C,
        m=LCG_M,
        count=config["OrdersParameters"]["total"],
    )

    notesIndexList = uniformDistributionRandomList(
        pseudorandom_numbers_from_0_to_1, a=0, b=len(config["Data"]["Notes"])
    )

    notesList = getValuesBasedOnIndexes(notesIndexList, config["Data"]["Notes"])

    logger.info("Generated notes")

    return notesList


def tagsGenerator(config):
    tagsRawList = [[] for _ in range(config["OrdersParameters"]["total"])]

    for tag_index in range(len(config["Data"]["Tags"])):
        pseudorandom_numbers_from_0_to_1 = pseudorandomList(
            seed=config["Seeds"]["Tags"] + tag_index,
            a=LCG_A,
            c=LCG_C,
            m=LCG_M,
            count=config["OrdersParameters"]["total"],
        )

        # Since uniformDistributionRandomList returns int values in range [a, b)
        b = 2

        # Array of 0 and 1. 0: False, 1: True
        isAllowedTag = uniformDistributionRandomList(
            pseudorandom_numbers_from_0_to_1, a=0, b=b
        )

        for order_index in range(config["OrdersParameters"]["total"]):
            if isAllowedTag[order_index]:
                tag = config["Data"]["Tags"][tag_index]
                tagsRawList[order_index].append(tag)

    tagsList = []
    for tags in tagsRawList:
        tagsList.append(",".join(tags))

    return tagsList


def statusGenerator(config):
    resultList = []
    incremeter = 1
    seed = config["Seeds"]["Status"]
    possibleStatuses = config["Data"]["Status"]

    for order_type in config["OrdersParameters"]["orders"]:

        statuses_count_order = len(order_type["Statuses"])

        pseudorandom_numbers_from_0_to_1 = pseudorandomList(
            seed=seed,
            a=LCG_A,
            c=LCG_C,
            m=LCG_M,
            count=order_type["count"] * statuses_count_order,
        )
        seed += incremeter

        for index in range(order_type["count"]):
            status_order_index = 0
            for status_type_index in order_type["Statuses"]:

                rundom_number_index = index * statuses_count_order + status_order_index

                pseudorandom_number_from_0_to_1 = pseudorandom_numbers_from_0_to_1[
                    rundom_number_index
                ]

                # statuses_type_count
                b = len(possibleStatuses[status_type_index])
                a = 0

                status_index = int((b - a) * pseudorandom_number_from_0_to_1 + a)
                status = possibleStatuses[status_type_index][status_index]
                resultList.append(status)

                status_order_index += 1

    return resultList


def datetimeGenerator(config):

    resultList = []
    incremeter = 1
    seed = config["Seeds"]["Datetime"]
    baseDatetime = datetime.strptime(
        config["Parameters"]["baseDatetime"], config["Parameters"]["baseDatetimeFormat"]
    )

    for order_type in config["OrdersParameters"]["orders"]:

        number_datetime_values_order = len(order_type["Statuses"])

        random_numbers, incremeter = getRandomNumbersDatetime(
            seed, order_type["count"], incremeter, number_datetime_values_order
        )

        for order_index in range(order_type["count"]):
            datetime_order_list = getDatetimeListAppend(
                config["Parameters"]["timeFrameMilliseconds"],
                number_datetime_values_order,
                order_index,
                random_numbers,
                baseDatetime,
            )
            resultList.extend(datetime_order_list)

    return resultList


def getDatetimeListAppend(
    timeFrame, number_datetime_values_order, order_index, random_numbers, baseDatetime
):
    resultList = []
    order_datetimes = []
    timedeltaMilliseconds = 0
    for datetime_number_order in range(number_datetime_values_order):
        millisecondsDelta = int(
            timeFrame * random_numbers[order_index][datetime_number_order]
        )

        timeFrame -= millisecondsDelta
        timedeltaMilliseconds += millisecondsDelta

        datetimeToAppend = baseDatetime + timedelta(milliseconds=timedeltaMilliseconds)
        datetimeToAppendFormated = datetimeToAppend.strftime(DATETIME_FORMAT)[:-3]
        resultList.append(datetimeToAppendFormated)

    return resultList


def getFormatedData(
    config,
    idList,
    sideList,
    instrumentList,
    px_InitList,
    px_FillList,
    volume_InitList,
    volume_FillList,
    notesList,
    tagsList,
    statusList,
):

    # Dependent lists
    px_FillList = repeatRecordsValuesBasedOnStatus(
        config, px_FillList, px_InitList, statusList, isPrice=True
    )
    volume_FillList = repeatRecordsValuesBasedOnStatus(
        config, volume_FillList, volume_InitList, statusList
    )

    # Independent lists
    idList = repeatRecordsValues(config, idList)
    sideList = repeatRecordsValues(config, sideList)
    instrumentList = repeatRecordsValues(config, instrumentList)
    px_InitList = repeatRecordsValues(config, px_InitList)
    volume_InitList = repeatRecordsValues(config, volume_InitList)
    notesList = repeatRecordsValues(config, notesList)
    tagsList = repeatRecordsValues(config, tagsList)

    return (
        idList,
        sideList,
        instrumentList,
        px_InitList,
        px_FillList,
        volume_InitList,
        volume_FillList,
        notesList,
        tagsList,
    )


def generateData(config):

    logger.info("Starting generate data")
    # Not formated
    idList = idGenerator(config)
    sideList = sideGenerator(config)
    instrumentList, instrumentIndexList = instrumentGenerator(config)
    px_InitList, px_InitRawList = px_InitGenerator(config, instrumentIndexList)
    px_FillList = px_FillGenerator(config, px_InitRawList)
    volume_InitList = volume_InitGenerator(config)
    volume_FillList = volume_FillGenerator(config, volume_InitList)
    notesList = notesGenerator(config)
    tagsList = tagsGenerator(config)

    # Already formated
    statusList = statusGenerator(config)
    datetimeList = datetimeGenerator(config)

    logger.info("Finished generating data. Starting formatting data")

    (
        idList,
        sideList,
        instrumentList,
        px_InitList,
        px_FillList,
        volume_InitList,
        volume_FillList,
        notesList,
        tagsList,
    ) = getFormatedData(
        config,
        idList,
        sideList,
        instrumentList,
        px_InitList,
        px_FillList,
        volume_InitList,
        volume_FillList,
        notesList,
        tagsList,
        statusList,
    )

    logger.info("Finished formatting data")

    return (
        idList,
        sideList,
        instrumentList,
        px_InitList,
        px_FillList,
        volume_InitList,
        volume_FillList,
        notesList,
        tagsList,
        statusList,
        datetimeList,
    )
