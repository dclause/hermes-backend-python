export declare type GroupDeviceConfigurationProperties = {
  board: number,
  device: number,
  order: number,
}
export declare type GroupConfigurationProperties = {
  id: number,
  name?: string,
  parent: number,
  layout: string,
  order: number,
  content: GroupDeviceConfigurationProperties[],
}