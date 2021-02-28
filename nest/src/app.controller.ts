import { Controller, Get, Inject, Logger } from '@nestjs/common';
import { ClientProxy, EventPattern } from '@nestjs/microservices';
import { AppService } from './app.service';

@Controller()
export class AppController {
  private readonly logger = new Logger(AppController.name);

  constructor(
    private readonly appService: AppService,
    @Inject('RuntimeClient') private readonly runtimeClient: ClientProxy,
  ) {}

  @Get()
  getHello(): string {
    this.runtimeClient.emit('test', {
      foo: 'task id',
      bar: 'user id',
    });

    this.logger.log('task sent');

    return this.appService.getHello();
  }

  @EventPattern('result')
  async getResult(data) {
    this.logger.log(data);
  }
}
