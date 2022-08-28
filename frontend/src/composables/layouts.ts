import ConnectedLayout from "@/layouts/ConnectedLayout.vue";
import SimpleLayout from "@/layouts/SimpleLayout.vue";

export type ProtocolConfigurationProperties = {
  id: number,
  name?: string,
  controller: string,
  [x: string]: unknown;
}

/**
 * Returns the layout to use among available list.
 * Defaults to ConnectedLayout if not given.
 *
 * @note: this is done to avoid lazy-loading components.
 * It may seem opposite to usual performance recommendations, but we want here
 * to avoid any extra server work or network load once the UI is started, hence
 * we are okay with a longer initial load time.
 */
export function useLayout(layout: string): unknown {
  const layouts: Record<string, unknown> = {
    ConnectedLayout: ConnectedLayout,
    SimpleLayout: SimpleLayout
  };
  return layouts[layout] ?? ConnectedLayout;
}

