from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    # rabbitmq
    rabbitmq_username: str = Field("guest")
    rabbitmq_password: str = Field("guest")
    rabbitmq_host: str = Field("localhost")
    rabbitmq_port: int = Field(5672)
    rabbitmq_vhost: str = Field("/")

    # redis
    redis_username: str = Field("default")
    redis_password: str = Field("")
    redis_host: str = Field("localhost")
    redis_port: int = Field(6379)
    redis_db: int = Field(0)

    # postgres
    postgres_host: str = Field("localhost")
    postgres_port: int = Field(5432)
    postgres_db: str = Field("payment_processing")
    postgres_user: str = Field("payment_processing")
    postgres_password: str = Field("payment_processing")

    # sqlalchemy
    sa_debug: bool = Field(False)
    sa_pool_size: int = Field(50)
    sa_max_overflow: int = Field(-1)
    sa_pool_timeout: float = Field(30.0)
    sa_pool_recycle: int = Field(600)
    sa_pool_use_lifo: bool = Field(False)
    sa_pool_pre_ping: bool = Field(True)

    # common
    debug: bool = Field(False, description="Флаг отладки")

    # backend
    backend_base_url: str = Field("http://localhost:8000", description="Основной URL")
    backend_api_prefix: str = Field("/api/v1", description="Префикс")
    backend_cors_allow_origin: str = Field("*", description="Список разрешенных доменов для CORS")
    backend_authentication_header_key: str = Field(description="Заголовок с ключом API")
    backend_authentication_header_value: str = Field(description="Значение ключа API")
    backend_payment_success_rate: float = Field(0.9)
    backend_payment_min_delay: int = Field(2)
    backend_payment_max_delay: int = Field(5)
    backend_webhook_retry_attempts: int = Field(3)
    backend_webhook_request_timeout: float = Field(10)
    backend_webhook_retry_delay_base: float = Field(1.0)
    backend_outbox_poll_interval: float = Field(2.0)

    # consumer
    consumer_exchange_name: str = Field("payments")
    consumer_payment_routing_key: str = Field("payment.created")
    consumer_queue_name: str = Field("payments.new")
    consumer_queue_delivery_limit: int = Field(3)
    consumer_dlx_exchange_name: str = Field("payments.dlx")
    consumer_dead_letter_routing_key: str = Field("dlq")
    consumer_dlq_queue_name: str = Field("payments.new.dlq")
    consumer_dlq_queue_message_ttl: int = Field(604800000)

    def get_redis_url(self) -> str:
        """Получение URL подключения к серверу Redis"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    def get_rabbitmq_url(self) -> str:
        """Получение URL подключения к серверу RabbitMQ"""
        return (
            f"amqp://{self.rabbitmq_username}:{self.rabbitmq_password}@"
            f"{self.rabbitmq_host}:{self.rabbitmq_port}{self.rabbitmq_vhost}"
        )

    def get_postgres_url(self) -> str:
        """Получение URL подключения к серверу PostgreSQL"""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = AppSettings()
