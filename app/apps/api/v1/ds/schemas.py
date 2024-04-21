from enum import Enum

from pydantic import BaseModel, Field

from app.apps.schemas import ApiResponseSchema


class TaskStatusChoices(str, Enum):
    SUCCESS: str = "SUCCESS"
    FAILURE: str = "FAILURE"


class DsTaskCreatedResponse(ApiResponseSchema):
    task_id: str
    ds_record_id: str = Field(alias="DsRecordId", default="")


class DsTaskResult(BaseModel):
    task_status: TaskStatusChoices
    barcode: str | None
    final_photo: str | bytes | None
    final_photo_format: str
    errors: list[str]


class DsTaskFailRequestSchema(ApiResponseSchema):
    task_id: str


class DsTaskStatusResponse(DsTaskCreatedResponse, DsTaskResult):
    pass


class DsStepsBodyData(BaseModel):
    Id: str
    DsRecordId: str


class DsFirstStepBody(DsStepsBodyData):
    ctl00_SiteContentPlaceHolder_ucLocation_ddlLocation: str | None
    ctl00_SiteContentPlaceHolder_ddlQuestions: str | None
    ctl00_SiteContentPlaceHolder_txtAnswer: str | None


class DsSecondStepBody(DsStepsBodyData):
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_SURNAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_GIVEN_NAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_FULL_NAME_NATIVE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexAPP_FULL_NAME_NATIVE_NA: bool | None
    other_names_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblOtherNames"
    )
    ctl00_SiteContentPlaceHolder_FormView1_DListAlias_ctl00_tbxSURNAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListAlias_ctl00_tbxGIVEN_NAME: str | None
    tele_code_question_radio: bool = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblTelecodeQuestion"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_TelecodeSURNAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_TelecodeGIVEN_NAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlAPP_GENDER: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlAPP_MARITAL_STATUS: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlDOBDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlDOBMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxDOBYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_POB_CITY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_POB_ST_PROVINCE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexAPP_POB_ST_PROVINCE_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlAPP_POB_CNTRY: str | None


class DsThirdStepBody(DsStepsBodyData):
    ctl00_SiteContentPlaceHolder_FormView1_ddlAPP_NATL: str | None
    country_btn: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblAPP_OTH_NATL_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlOTHER_NATL_ctl00_ddlOTHER_NATL: str | None
    passport_second_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$dtlOTHER_NATL$ctl00$rblOTHER_PPT_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlOTHER_NATL_ctl00_tbxOTHER_PPT_NUM: str | None
    other_cntry_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPermResOtherCntryInd"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlOthPermResCntry_ctl00_ddlOthPermResCntry: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_NATIONAL_ID: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexAPP_NATIONAL_ID_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_SSN: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexAPP_SSN_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_TAX_ID: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexAPP_TAX_ID_NA: bool | None


class DsFourthStepBody(DsStepsBodyData):
    ctl00_SiteContentPlaceHolder_FormView1_dlPrincipalAppTravel_ctl00_ddlOtherPurpose: str | None
    specific_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblSpecificTravel"
    )
    ctl00_SiteContentPlaceHolder_FormView1_ddlARRIVAL_US_DTEDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlARRIVAL_US_DTEMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxARRIVAL_US_DTEYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxArriveFlight: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxArriveCity: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlDEPARTURE_US_DTEDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlDEPARTURE_US_DTEMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxDEPARTURE_US_DTEYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxDepartFlight: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxDepartCity: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlTravelLoc_ctl00_tbxSPECTRAVEL_LOCATION: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxStreetAddress1: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxStreetAddress2: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxCity: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlTravelState: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbZIPCode: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlTRAVEL_DTEDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlTRAVEL_DTEMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxTRAVEL_DTEYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxTRAVEL_LOS: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlTRAVEL_LOS_CD: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlWhoIsPaying: str | None


class DsFifthStepBody(DsStepsBodyData):
    travel_with_your_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblOtherPersonsTravelingWithYou"
    )
    group_travel_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblGroupTravel"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxGroupName: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dlTravelCompanions_ctl00_tbxSurname: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dlTravelCompanions_ctl00_tbxGivenName: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dlTravelCompanions_ctl00_ddlTCRelationship: str | None


class DsSixStepBody(DsStepsBodyData):
    prev_travel_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPREV_US_TRAVEL_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlPREV_US_VISIT_ctl00_ddlPREV_US_VISIT_DTEDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPREV_US_VISIT_ctl00_ddlPREV_US_VISIT_DTEMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPREV_US_VISIT_ctl00_tbxPREV_US_VISIT_DTEYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPREV_US_VISIT_ctl00_tbxPREV_US_VISIT_LOS: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPREV_US_VISIT_ctl00_ddlPREV_US_VISIT_LOS_CD: str | None
    us_driver_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPREV_US_DRIVER_LIC_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlUS_DRIVER_LICENSE_ctl00_tbxUS_DRIVER_LICENSE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlUS_DRIVER_LICENSE_ctl00_cbxUS_DRIVER_LICENSE_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlUS_DRIVER_LICENSE_ctl00_ddlUS_DRIVER_LICENSE_STATE: str | None
    prev_visa_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPREV_VISA_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_ddlPREV_VISA_ISSUED_DTEDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlPREV_VISA_ISSUED_DTEMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxPREV_VISA_ISSUED_DTEYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxPREV_VISA_FOIL_NUMBER: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxPREV_VISA_FOIL_NUMBER_NA: bool | None
    visa_same_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPREV_VISA_SAME_TYPE_IND"
    )
    visa_same_cntry_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPREV_VISA_SAME_CNTRY_IND"
    )
    visa_ten_prstr_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPREV_VISA_TEN_PRINT_IND"
    )
    visa_lost_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPREV_VISA_LOST_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxPREV_VISA_LOST_YEAR: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxPREV_VISA_LOST_EXPL: str | None
    visa_cancelled_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPREV_VISA_CANCELLED_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxPREV_VISA_CANCELLED_EXPL: str | None
    
    visa_refused_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPREV_VISA_REFUSED_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxPREV_VISA_REFUSED_EXPL: str | None
   
    estavisa_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblVWP_DENIAL_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxVWP_DENIAL_EXPL: str | None

    petition_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblIV_PETITION_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxIV_PETITION_EXPL: str | None


class DsSevenStepBody(DsStepsBodyData):
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_ADDR_LN1: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_ADDR_LN2: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_ADDR_CITY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_ADDR_STATE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexAPP_ADDR_STATE_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_ADDR_POSTAL_CD: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexAPP_ADDR_POSTAL_CD_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlCountry: str | None
    mailing_addr_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblMailingAddrSame"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxMAILING_ADDR_LN1: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxMAILING_ADDR_LN2: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxMAILING_ADDR_CITY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxMAILING_ADDR_STATE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexMAILING_ADDR_STATE_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxMAILING_ADDR_POSTAL_CD: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexMAILING_ADDR_POSTAL_CD_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlMailCountry: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_HOME_TEL: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_MOBILE_TEL: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexAPP_MOBILE_TEL_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_BUS_TEL: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexAPP_BUS_TEL_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_rblAddPhone: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlAddPhone_ctl00_tbxAddPhoneInfo: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_EMAIL_ADDR: str | None
    add_email_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblAddEmail"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlAddEmail_ctl00_tbxAddEmailInfo: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlSocial_ctl00_ddlSocialMedia: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlSocial_ctl00_tbxSocialMediaIdent: str | None
    add_social_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblAddSocial"
    )
    add_social_plat_radio: bool | str | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$dtlAddSocial$ctl00$tbxAddSocialPlat"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlAddSocial_ctl00_tbxAddSocialHand: str | None


class DsEightStepBody(DsStepsBodyData):
    ctl00_SiteContentPlaceHolder_FormView1_ddlPPT_TYPE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxPPT_NUM: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxPPT_BOOK_NUM: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexPPT_BOOK_NUM_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlPPT_ISSUED_CNTRY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxPPT_ISSUED_IN_CITY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxPPT_ISSUED_IN_STATE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlPPT_ISSUED_IN_CNTRY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlPPT_ISSUED_DTEDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlPPT_ISSUED_DTEMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxPPT_ISSUEDYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlPPT_EXPIRE_DTEDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlPPT_EXPIRE_DTEMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxPPT_EXPIREYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxPPT_EXPIRE_NA: bool | None
    lost_ppt_str_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblLOST_PPT_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlLostPPT_ctl00_tbxLOST_PPT_NUM: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlLostPPT_ctl00_cbxLOST_PPT_NUM_UNKN_IND: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlLostPPT_ctl00_ddlLOST_PPT_NATL: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlLostPPT_ctl00_tbxLOST_PPT_EXPL: str | None


class DsNineStepBody(DsStepsBodyData):
    ctl00_SiteContentPlaceHolder_FormView1_tbxUS_POC_SURNAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxUS_POC_GIVEN_NAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxUS_POC_ORGANIZATION: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxUS_POC_NAME_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxUS_POC_ORG_NA_IND: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlUS_POC_REL_TO_APP: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxUS_POC_ADDR_LN1: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxUS_POC_ADDR_LN2: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxUS_POC_ADDR_CITY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlUS_POC_ADDR_STATE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxUS_POC_ADDR_POSTAL_CD: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxUS_POC_HOME_TEL: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxUS_POC_EMAIL_ADDR: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexUS_POC_EMAIL_ADDR_NA: bool | None


class DsTenStepBody(DsStepsBodyData):
    ctl00_SiteContentPlaceHolder_FormView1_tbxFATHER_SURNAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxFATHER_SURNAME_UNK_IND: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxFATHER_GIVEN_NAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxFATHER_GIVEN_NAME_UNK_IND: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlFathersDOBDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlFathersDOBMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxFathersDOBYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxFATHER_DOB_UNK_IND: bool | None
    live_in_us_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblFATHER_LIVE_IN_US_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_ddlFATHER_US_STATUS: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxMOTHER_SURNAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxMOTHER_SURNAME_UNK_IND: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxMOTHER_GIVEN_NAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxMOTHER_GIVEN_NAME_UNK_IND: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlMothersDOBDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlMothersDOBMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxMothersDOBYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxMOTHER_DOB_UNK_IND: bool | None
    mother_lives_in_us_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblMOTHER_LIVE_IN_US_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_ddlMOTHER_US_STATUS: str | None
    us_immed_status_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblUS_IMMED_RELATIVE_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dlUSRelatives_ctl00_tbxUS_REL_SURNAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dlUSRelatives_ctl00_tbxUS_REL_GIVEN_NAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dlUSRelatives_ctl00_ddlUS_REL_TYPE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dlUSRelatives_ctl00_ddlUS_REL_STATUS: str | None
    other_relative_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblUS_OTHER_RELATIVE_IND"
    )


class DsElevenStepBody(DsStepsBodyData):
    ctl00_SiteContentPlaceHolder_FormView1_tbxSpouseSurname: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxSpouseGivenName: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlDOBDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlDOBMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxDOBYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxSpousePOBCity: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlSpouseNatDropDownList: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexSPOUSE_POB_CITY_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlSpousePOBCountry: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlSpouseAddressType: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxSPOUSE_ADDR_LN1: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxSPOUSE_ADDR_LN2: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxSPOUSE_ADDR_CITY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxSPOUSE_ADDR_STATE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexSPOUSE_ADDR_STATE_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxSPOUSE_ADDR_POSTAL_CD:bool | None
    ctl00_SiteContentPlaceHolder_FormView1_cbexSPOUSE_ADDR_POSTAL_CD_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlSPOUSE_ADDR_CNTRY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxNumberOfPrevSpouses: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_tbxSURNAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_tbxGIVEN_NAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_ddlDOBDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_ddlDOBMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_tbxDOBYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_ddlSpouseNatDropDownList: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_tbxSpousePOBCity: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_cbxSPOUSE_POB_CITY_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_ddlSpousePOBCountry: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_ddlDomDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_ddlDomMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_txtDomYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_ddlDomEndDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_ddlDomEndMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_txtDomEndYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_tbxHowMarriageEnded: str | None
    ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_ddlMarriageEnded_CNTRY: str | None
	

class DsTwelveStepBody(DsStepsBodyData):
    ctl00_SiteContentPlaceHolder_FormView1_ddlPresentOccupation: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxEmpSchName: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxEmpSchAddr1: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxEmpSchAddr2: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxEmpSchCity: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxWORK_EDUC_ADDR_STATE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxWORK_EDUC_ADDR_STATE_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxWORK_EDUC_ADDR_POSTAL_CD: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxWORK_EDUC_ADDR_POSTAL_CD_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxWORK_EDUC_TEL: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlEmpSchCountry: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlEmpDateFromDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_ddlEmpDateFromMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxEmpDateFromYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxCURR_MONTHLY_SALARY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_cbxCURR_MONTHLY_SALARY_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_tbxDescribeDuties: str | None


class DsThirtyStepBody(DsStepsBodyData):
    employed_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPreviouslyEmployed"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbEmployerName: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbEmployerStreetAddress1: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbEmployerStreetAddress2: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbEmployerCity: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbxPREV_EMPL_ADDR_STATE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_cbxPREV_EMPL_ADDR_STATE_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbxPREV_EMPL_ADDR_POSTAL_CD: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_cbxPREV_EMPL_ADDR_POSTAL_CD_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_DropDownList2: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbEmployerPhone: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbJobTitle: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbSupervisorSurname: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_cbxSupervisorSurname_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbSupervisorGivenName: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_cbxSupervisorGivenName_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_ddlEmpDateFromDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_ddlEmpDateFromMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbxEmpDateFromYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_ddlEmpDateToDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_ddlEmpDateToMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbxEmpDateToYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEmpl_ctl00_tbDescribeDuties: str | None
    other_educ_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblOtherEduc"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_tbxSchoolName: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_tbxSchoolAddr1: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_tbxSchoolAddr2: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_tbxSchoolCity: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_tbxEDUC_INST_ADDR_STATE: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_cbxEDUC_INST_ADDR_STATE_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_tbxEDUC_INST_POSTAL_CD: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_cbxEDUC_INST_POSTAL_CD_NA: bool | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_ddlSchoolCountry: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_tbxSchoolCourseOfStudy: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_ddlSchoolFromDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_ddlSchoolFromMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_tbxSchoolFromYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_ddlSchoolToDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_ddlSchoolToMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlPrevEduc_ctl00_tbxSchoolToYear: str | None


class DsFourthlyStepBody(DsStepsBodyData):
    clan_tribe_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblCLAN_TRIBE_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxCLAN_TRIBE_NAME: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlLANGUAGES_ctl00_tbxLANGUAGE_NAME: str | None
    visited_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblCOUNTRIES_VISITED_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlCountriesVisited_ctl00_ddlCOUNTRIES_VISITED: str | None
    organization_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblORGANIZATION_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlORGANIZATIONS_ctl00_tbxORGANIZATION_NAME: str | None
    taliban_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblTALIBAN_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxTALIBAN_EXPL: str | None
    skills_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblSPECIALIZED_SKILLS_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxSPECIALIZED_SKILLS_EXPL: str | None
    service_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblMILITARY_SERVICE_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_dtlMILITARY_SERVICE_ctl00_ddlMILITARY_SVC_CNTRY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlMILITARY_SERVICE_ctl00_tbxMILITARY_SVC_BRANCH: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlMILITARY_SERVICE_ctl00_tbxMILITARY_SVC_RANK: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlMILITARY_SERVICE_ctl00_tbxMILITARY_SVC_SPECIALTY: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlMILITARY_SERVICE_ctl00_ddlMILITARY_SVC_FROMDay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlMILITARY_SERVICE_ctl00_ddlMILITARY_SVC_FROMMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlMILITARY_SERVICE_ctl00_tbxMILITARY_SVC_FROMYear: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlMILITARY_SERVICE_ctl00_ddlMILITARY_SVC_TODay: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlMILITARY_SERVICE_ctl00_ddlMILITARY_SVC_TOMonth: str | None
    ctl00_SiteContentPlaceHolder_FormView1_dtlMILITARY_SERVICE_ctl00_tbxMILITARY_SVC_TOYear: str | None
    org_ind_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblINSURGENT_ORG_IND"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxINSURGENT_ORG_EXPL: str | None


class DsFifthlyStepBody(DsStepsBodyData):
    disease_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblDisease"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxDisease: str | None
    disorder_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblDisorder"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxDisorder: str | None
    drug_user_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblDruguser"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxDruguser: str | None


class DsSixthStepBody(DsStepsBodyData):
    arrested_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblArrested"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxArrested: str | None
    substanced_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblControlledSubstances"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxControlledSubstances: str | None
    prostitution_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblProstitution"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxProstitution: str | None
    money_laundering_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblMoneyLaundering"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxMoneyLaundering: str | None
    human_traffic_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblHumanTrafficking"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxHumanTrafficking: str | None
    assisted_traffic_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblAssistedSevereTrafficking"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxAssistedSevereTrafficking: str | None
    human_traffic_related_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblHumanTraffickingRelated"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxHumanTraffickingRelated: str | None


class DsSeventhStepBody(DsStepsBodyData):
    illegal_activity_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblIllegalActivity"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxIllegalActivity: str | None
    terrorist_activity_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblTerroristActivity"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxTerroristActivity: str | None
    terrorist_support_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblTerroristSupport"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxTerroristSupport: str | None
    terrorist_org_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblTerroristOrg"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxTerroristOrg: str | None
    terrorist_rel_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblTerroristRel"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxTerroristRel: str | None
    genocide_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblGenocide"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxGenocide: str | None
    torture_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblTorture"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxTorture: str | None
    violence_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblExViolence"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxExViolence: str | None
    child_soldier_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblChildSoldier"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxChildSoldier: str | None
    religious_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblReligiousFreedom"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxReligiousFreedom: str | None
    population_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblPopulationControls"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxPopulationControls: str | None
    transplant_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblTransplant"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxTransplant: str | None


class DsEighthStepBody(DsStepsBodyData):
    hearing_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblRemovalHearing"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxRemovalHearing: str | None
    fraud_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblImmigrationFraud"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxImmigrationFraud: str | None
    attend_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblFailToAttend"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxFailToAttend: str | None
    violation_btn: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblVisaViolation"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxVisaViolation: str | None
    deport_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblDeport"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxDeport_EXPL: str | None


class DsNinetyStepBody(DsStepsBodyData):
    child_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblChildCustody"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxChildCustody: str | None
    violation_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblVotingViolation"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxVotingViolation: str | None
    renounce_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblRenounceExp"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxRenounceExp: str | None
    reimb_radio: bool | None = Field(
        alias="ctl00$SiteContentPlaceHolder$FormView1$rblAttWoReimb"
    )
    ctl00_SiteContentPlaceHolder_FormView1_tbxAttWoReimb: str | None


class DsStepsData(BaseModel):
    step_1: DsFirstStepBody | None = None
    step_2: DsSecondStepBody | None = None
    step_3: DsThirdStepBody | None = None
    step_4: DsFourthStepBody | None = None
    step_5: DsFifthStepBody | None = None
    step_6: DsSixStepBody | None = None
    step_7: DsSevenStepBody | None = None
    step_8: DsEightStepBody | None = None
    step_9: DsNineStepBody | None = None
    step_10: DsTenStepBody | None = None
    step_11: DsElevenStepBody | None = None
    step_12: DsTwelveStepBody | None = None
    step_13: DsThirtyStepBody | None = None
    step_14: DsFourthlyStepBody | None = None
    step_15: DsFifthlyStepBody | None = None
    step_16: DsSixthStepBody | None = None
    step_17: DsSeventhStepBody | None = None
    step_18: DsEighthStepBody | None = None
    step_19: DsNinetyStepBody | None = None


class DsTaskCreateBody(BaseModel):
    id: str
    barcode: str = ""
    user_id: str
    steps: DsStepsData
    photo: str
    photo_format: str
