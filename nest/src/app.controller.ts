import { Controller, Get, Inject, Logger } from '@nestjs/common';
import { ClientProxy, EventPattern } from '@nestjs/microservices';
import { AppService } from './app.service';

@Controller()
export class AppController {
  private readonly logger = new Logger(AppController.name);
  constructor(
    private readonly appService: AppService,
    @Inject('TEST_SERVICE') private readonly client: ClientProxy,
  ) {}

  @Get()
  getHello(): string {
    this.client.emit('exec', {
      task: 'task id',
      user: 'user id',
      answer: `print('hello')`,
      tests: 'some tests',
    });
    this.logger.log('task sent');
    return this.appService.getHello();
  }
  @EventPattern('result')
  async getResult(data: string) {
    this.logger.log(data);
  }
}
