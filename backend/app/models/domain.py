"""Shared enumerations and constants for the dental clinic domain."""

from enum import StrEnum


class DentalService(StrEnum):
    """Available dental services at QuensultingAI Dental Clinic."""

    DENTAL_CLEANING = "dental_cleaning"
    ROOT_CANAL_TREATMENT = "root_canal_treatment"
    TEETH_WHITENING = "teeth_whitening"
    BRACES_CONSULTATION = "braces_consultation"
    TOOTH_EXTRACTION = "tooth_extraction"
    GENERAL_DENTAL_CONSULTATION = "general_dental_consultation"


class TransferReason(StrEnum):
    """Reasons for transferring a caller to a human agent."""

    CALLER_REQUESTED = "caller_requested"
    EMERGENCY = "emergency"
    MAX_RETRIES_EXCEEDED = "max_retries_exceeded"
    BOOKING_FAILURE = "booking_failure"
    OTHER = "other"


# ---- Clinic metadata -------------------------------------------------------

CLINIC_NAME = "QuensultingAI Dental Clinic"
CLINIC_LOCATION = "Baner, Pune"
CLINIC_PHONE = "+91-20-XXXX-XXXX"

CONSULTATION_FEE_INR = 500

PAYMENT_METHODS = ["Cash", "UPI", "Credit Card", "Debit Card"]

WORKING_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

WORKING_HOURS_START = 9   # 9:00 AM
WORKING_HOURS_END = 18    # 6:00 PM (exclusive — last slot at 5 PM)

SERVICE_DISPLAY_NAMES: dict[DentalService, str] = {
    DentalService.DENTAL_CLEANING: "Dental Cleaning",
    DentalService.ROOT_CANAL_TREATMENT: "Root Canal Treatment",
    DentalService.TEETH_WHITENING: "Teeth Whitening",
    DentalService.BRACES_CONSULTATION: "Braces Consultation",
    DentalService.TOOTH_EXTRACTION: "Tooth Extraction",
    DentalService.GENERAL_DENTAL_CONSULTATION: "General Dental Consultation",
}

# -- Response Messages -------------------------------------------------------

MSG_BOOKING_SUCCESS = "Appointment booked successfully for {name}."
MSG_CANCEL_SUCCESS = "Appointment for {name} has been cancelled."
MSG_RESCHEDULE_SUCCESS = "Appointment for {name} has been rescheduled to {date} at {time}."
