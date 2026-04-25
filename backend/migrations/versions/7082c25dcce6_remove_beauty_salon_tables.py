"""remove_beauty_salon_tables

Revision ID: 7082c25dcce6
Revises: cbdfdb50e48d
Create Date: 2026-04-23 13:42:19.794003

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7082c25dcce6"
down_revision: Union[str, Sequence[str], None] = "cbdfdb50e48d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Eliminar FKs y constraints que dependen de las tablas a eliminar
    op.drop_constraint(
        "business_hours_collaborator_id_fkey",
        table_name="business_hours",
        type_="foreignkey",
        if_exists=True,
    )
    op.drop_constraint(
        "clients_current_collaborator_id_fkey",
        table_name="clients",
        type_="foreignkey",
        if_exists=True,
    )
    op.drop_constraint(
        "collaborator_departments_collaborator_id_fkey",
        table_name="collaborator_departments",
        type_="foreignkey",
        if_exists=True,
    )

    # 2. Eliminar índices y constraints de business_hours
    op.drop_index(
        "ix_business_hours_collaborator_id", table_name="business_hours", if_exists=True
    )
    op.drop_constraint(
        "_day_collaborator_uc",
        table_name="business_hours",
        type_="unique",
        if_exists=True,
    )
    op.drop_column("business_hours", "collaborator_id", if_exists=True)

    # 3. Eliminar tablas en orden correcto (dependencias primero)
    op.drop_table("collaborator_departments", if_exists=True)
    op.drop_table("appointments", if_exists=True)
    op.drop_table(
        "scheduled_reminders", if_exists=True
    )  # Se recreará sin FK a appointments
    op.drop_table("services", if_exists=True)
    op.drop_table("collaborators", if_exists=True)

    # 4. Eliminar columna de clients que referenciaba a collaborators
    op.drop_column("clients", "current_collaborator_id", if_exists=True)

    # 5. Crear nueva constraint para restaurant
    op.create_unique_constraint("_day_restaurant_uc", "business_hours", ["day_of_week"])


def downgrade() -> None:
    """Downgrade schema."""
    # Recrear tablas del sistema de peluquería
    op.create_table(
        "collaborators",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=True),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.Column("collaborator_id", sa.Integer(), nullable=False),
        sa.Column("client_name", sa.String(length=100), nullable=False),
        sa.Column("client_phone", sa.String(length=20), nullable=True),
        sa.Column("client_email", sa.String(length=255), nullable=True),
        sa.Column("client_notes", sa.Text(), nullable=True),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "SCHEDULED",
                "CONFIRMED",
                "IN_PROGRESS",
                "COMPLETED",
                "CANCELLED",
                "NO_SHOW",
                name="appointmentstatus",
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(
            ["collaborator_id"], ["collaborators.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Restaurar FK en business_hours
    op.add_column(
        "business_hours", sa.Column("collaborator_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "fk_business_hours_collaborator_id_collaborators",
        "business_hours",
        "collaborators",
        ["collaborator_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "ix_business_hours_collaborator_id", "business_hours", ["collaborator_id"]
    )
    op.create_unique_constraint(
        "_day_collaborator_uc", "business_hours", ["day_of_week", "collaborator_id"]
    )

    # Eliminar constraint de restaurant
    op.drop_constraint("_day_restaurant_uc", "business_hours", type_="uniqueconstraint")

    # Recrear scheduled_reminders con FK a appointments
    op.create_table(
        "scheduled_reminders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("appointment_id", sa.Integer(), nullable=False),
        sa.Column("reminder_type", sa.String(length=20), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["appointment_id"], ["appointments.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
