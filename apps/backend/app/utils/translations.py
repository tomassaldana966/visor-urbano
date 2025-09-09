"""
Translation utilities for email notifications and messages
"""
from typing import Dict, Any, Optional

# Status text translations
STATUS_TRANSLATIONS = {
    "es": {
        0: "En Proceso",
        1: "Pendiente de Revisión", 
        2: "Aprobado",
        3: "Requiere Atención",
        4: "En Revisión",
        7: "Licencia Emitida"
    },
    "en": {
        0: "In Process",
        1: "Pending Review",
        2: "Approved", 
        3: "Requires Attention",
        4: "Under Review",
        7: "License Issued"
    },
    "pt": {
        0: "Em Processo",
        1: "Pendente de Revisão",
        2: "Aprovado",
        3: "Requer Atenção", 
        4: "Em Revisão",
        7: "Licença Emitida"
    },
    "fr": {
        0: "En Cours",
        1: "En Attente de Révision",
        2: "Approuvé",
        3: "Nécessite une Attention",
        4: "En Révision", 
        7: "Licence Émise"
    }
}

# Email subject translations
EMAIL_SUBJECTS = {
    "es": {
        "approved": "✅ Trámite Aprobado - Folio: {folio}",
        "rejected": "❌ Trámite Rechazado - Folio: {folio}",
        "license_issued": "🎉 Licencia Emitida - Folio: {folio}",
        "status_update": "📋 Actualización de Estado - Folio: {folio}",
        "license_download": "🎉 Tu Licencia Está Lista para Descarga - Folio: {folio}"
    },
    "en": {
        "approved": "✅ Procedure Approved - Folio: {folio}",
        "rejected": "❌ Procedure Rejected - Folio: {folio}",
        "license_issued": "🎉 License Issued - Folio: {folio}",
        "status_update": "📋 Status Update - Folio: {folio}",
        "license_download": "🎉 Your License is Ready for Download - Folio: {folio}"
    },
    "pt": {
        "approved": "✅ Procedimento Aprovado - Folio: {folio}",
        "rejected": "❌ Procedimento Rejeitado - Folio: {folio}",
        "license_issued": "🎉 Licença Emitida - Folio: {folio}",
        "status_update": "📋 Atualização de Status - Folio: {folio}",
        "license_download": "🎉 Sua Licença Está Pronta para Download - Folio: {folio}"
    },
    "fr": {
        "approved": "✅ Procédure Approuvée - Folio: {folio}",
        "rejected": "❌ Procédure Rejetée - Folio: {folio}",
        "license_issued": "🎉 Licence Émise - Folio: {folio}",
        "status_update": "📋 Mise à Jour du Statut - Folio: {folio}",
        "license_download": "🎉 Votre Licence est Prête pour Téléchargement - Folio: {folio}"
    }
}

# Notification messages
NOTIFICATION_MESSAGES = {
    "es": {
        "status_change": "Tu trámite {folio} ha cambiado de estado a: {status_text}",
        "status_change_with_reason": "Tu trámite {folio} ha cambiado de estado a: {status_text}. Motivo: {reason}",
        "license_ready": "¡Tu licencia del trámite {folio} está lista para descarga!"
    },
    "en": {
        "status_change": "Your procedure {folio} has changed status to: {status_text}",
        "status_change_with_reason": "Your procedure {folio} has changed status to: {status_text}. Reason: {reason}",
        "license_ready": "Your license for procedure {folio} is ready for download!"
    },
    "pt": {
        "status_change": "Seu procedimento {folio} mudou de status para: {status_text}",
        "status_change_with_reason": "Seu procedimento {folio} mudou de status para: {status_text}. Motivo: {reason}",
        "license_ready": "Sua licença do procedimento {folio} está pronta para download!"
    },
    "fr": {
        "status_change": "Votre procédure {folio} a changé de statut vers: {status_text}",
        "status_change_with_reason": "Votre procédure {folio} a changé de statut vers: {status_text}. Raison: {reason}",
        "license_ready": "Votre licence pour la procédure {folio} est prête pour téléchargement!"
    }
}

def get_status_text(status: int, language: str = "es") -> str:
    """Get human-readable status text in specified language"""
    return STATUS_TRANSLATIONS.get(language, STATUS_TRANSLATIONS["es"]).get(status, f"Estado {status}")

def get_email_subject(subject_type: str, folio: str, language: str = "es") -> str:
    """Get email subject in specified language"""
    subjects = EMAIL_SUBJECTS.get(language, EMAIL_SUBJECTS["es"])
    template = subjects.get(subject_type, subjects["status_update"])
    return template.format(folio=folio)

def get_notification_message(message_type: str, folio: str, status_text: str = "", reason: str = "", language: str = "es") -> str:
    """Get notification message in specified language"""
    messages = NOTIFICATION_MESSAGES.get(language, NOTIFICATION_MESSAGES["es"])
    
    if message_type == "status_change_with_reason" and reason:
        template = messages.get("status_change_with_reason", messages["status_change"])
        return template.format(folio=folio, status_text=status_text, reason=reason)
    elif message_type == "status_change":
        template = messages.get("status_change")
        return template.format(folio=folio, status_text=status_text)
    elif message_type == "license_ready":
        template = messages.get("license_ready")
        return template.format(folio=folio)
    
    return f"Notification for {folio}"

def get_user_language(user) -> str:
    """Get user's preferred language, default to Spanish"""
    if hasattr(user, 'language') and user.language:
        return user.language
    if hasattr(user, 'locale') and user.locale:
        return user.locale[:2]  # Extract language code from locale like 'en_US'
    return "es"  # Default to Spanish
