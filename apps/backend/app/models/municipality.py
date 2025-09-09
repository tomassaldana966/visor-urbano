from sqlalchemy import Column, BigInteger, String, DateTime, JSON, Integer, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class Municipality(Base):
    __tablename__ = 'municipalities'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    image = Column(String(250), nullable=True)
    director = Column(String(250), nullable=True)
    director_signature = Column(String(250), nullable=True)
    process_sheet = Column(Integer, nullable=True, default=1)
    solving_days = Column(Integer, nullable=True)
    issue_license = Column(Integer, nullable=True, default=0)
    address = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    responsible_area = Column(String(250), nullable=True)
    
    # License configuration fields
    allow_online_procedures = Column(Boolean, default=False, nullable=True)
    allow_window_reviewer_licenses = Column(Boolean, default=False, nullable=True)
    low_impact_license_cost = Column(String(255), nullable=True)
    license_additional_text = Column(Text, nullable=True)
    theme_color = Column(String(7), nullable=True)  # Color hexadecimal (#FFFFFF)
    
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    window_license_generation = Column(Integer, nullable=True, default=0)
    license_restrictions = Column(Text, nullable=True, default='')
    license_price = Column(String(255), nullable=True)
    initial_folio = Column(Integer, nullable=True)
    has_zoning = Column(Boolean, default=False, nullable=True)

    
    users = relationship("UserModel", back_populates="municipality", cascade="all, delete-orphan")
    requirements_queries = relationship("RequirementsQuery", back_populates="municipality", cascade="all, delete-orphan")
    user_roles = relationship("UserRoleModel", back_populates="municipality")
    sub_roles = relationship("SubRoleModel", back_populates="municipality", cascade="all, delete-orphan")
    technical_sheets = relationship("TechnicalSheet", back_populates="municipality", cascade="all, delete-orphan")
    business_licenses = relationship("BusinessLicense", back_populates="municipality")
    business_license_histories = relationship("BusinessLicenseHistory", back_populates="municipality")
    provisional_openings = relationship("ProvisionalOpening", back_populates="municipality")
    zoning_control_regulations = relationship("ZoningControlRegulation", back_populates="municipality")
    procedure_registrations = relationship("ProcedureRegistration", back_populates="municipality", cascade="all, delete-orphan")
    map_layers = relationship("MapLayer", secondary="maplayer_municipality", back_populates="municipalities")
    signatures = relationship("MunicipalitySignature", back_populates="municipality", cascade="all, delete-orphan", order_by="MunicipalitySignature.orden")
    fields = relationship("Field", back_populates="municipality")    
    zoning_impact_levels = relationship("ZoningImpactLevel", back_populates="municipality")
    requirements = relationship("Requirement", back_populates="municipality", cascade="all, delete-orphan")
        
    urban_development_zonings = relationship("UrbanDevelopmentZoning", back_populates="municipality", lazy="select")
    urban_development_zonings_standard = relationship("UrbanDevelopmentZoningStandard", back_populates="municipality", lazy="select")
    
    base_map_layer_associations = relationship("MunicipalityMapLayerBase", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
    neighborhoods = relationship("BaseNeighborhood", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
    localities = relationship("BaseLocality", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
    
    denue_records = relationship("EconomicUnitsDirectory", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
    
    inactive_businesses = relationship("InactiveBusiness", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
    business_sector_certificates = relationship("BusinessSectorCertificate", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
    business_sector_configurations = relationship("BusinessSectorConfiguration", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
    business_sector_impacts = relationship("BusinessSectorImpact", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
    building_footprints = relationship("BuildingFootprint", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
    land_parcel_mappings = relationship("LandParcelMapping", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
    
    dependency_reviews = relationship("DependencyReview", back_populates="municipality", cascade="all, delete-orphan", lazy="select")        
    blogs = relationship("Blog", back_populates="municipality", cascade="all, delete-orphan", lazy="select")
        
    departments = relationship("Department", back_populates="municipality", cascade="all, delete-orphan", lazy="select")


class MunicipalityGeom(Base):
    __tablename__ = 'municipality_geoms'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    municipality_id = Column(BigInteger, nullable=False, comment="Associated municipality ID")
    name = Column(String(250), nullable=False, comment="Municipality name")
    geom_type = Column(String(50), nullable=False, comment="Geometry type, e.g. 'Polygon'")
    coordinates = Column(JSON, nullable=False, comment="Coordinates in JSON format")
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())