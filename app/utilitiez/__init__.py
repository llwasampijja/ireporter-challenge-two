
        # # Test for creating an invalid red-flag missing one required parameter
        # An incident must contain all required fields, i.e: commment, title, images, and videos. It should not contain any other field except these.

        # RESP_INVALID_INCIDENT_INPUT)

        # # Test for creating an invalid red-flag with more parameters than needed
        # An incident must not contain any other parameters except those metioned

        # RESP_INVALID_INCIDENT_INPUT)

        # # Test for creating an invalid red-flag with string of vidoes instead of list
        # The images and videos fields must be lists of strings (urls)

        # RESP_INVALID_INCIDENT_INPUT)



        # # test add redflag with location with only one coordinate
        # RESP_INVALID_INCIDENT_INPUT)
        # The location field must be a string of two floating values separated by a comma ',', i.e: A latitude and longitude. Latitudes must be in the ranges 0 to 90 or -90 to 0. Longitudes must be in the ranges 0 to 180 or -180 to 0  

        # # test add redflag with location with coordinate not in range
        # RESP_INVALID_INCIDENT_INPUT)



        # # test add redflag with location with coordinate not in range
        # RESP_INVALID_INCIDENT_INPUT)

        # # Test update redflag with the wrong data type
        # RESP_INVALID_INCIDENT_INPUT)
        # The fields must 

        # # test update redflag which one never create

        # # test update red-flag with fields other than location'
        # RESP_INVALID_INCIDENT_INPUT)
