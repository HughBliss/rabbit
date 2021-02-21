import { NestFactory } from '@nestjs/core';
import { MicroserviceOptions, Transport } from '@nestjs/microservices';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const rabbitConnect = app.connectMicroservice<MicroserviceOptions>({
    transport: Transport.RMQ,
    options: {
      urls: ['amqp://user:password@localhost'],
      queue: 'results',
      queueOptions: {
        durable: false,
      },
    },
  });

  await app.startAllMicroservicesAsync();
  await app.listen(3000);
}
bootstrap();
