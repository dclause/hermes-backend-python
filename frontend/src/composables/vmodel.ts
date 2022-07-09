import type { Ref } from "vue";
import { computed, getCurrentInstance, ref } from "vue";

/**
 * Defines a composable to create a v-model compatible computed variable to be
 * used in wrapper component.
 *
 * @param props (object) The props of the components
 * @param propName (string) The name of the prop to use as a model.
 *
 * @note Currently, the propName has to be 'modelValue' exactly, hence the default value.
 * @see https://vuejs.org/guide/components/events.html#usage-with-v-model
 */
export function defineModel<Props extends object,
  Prop extends Extract<keyof Props, string>,
  Inner = Props[Prop]>(props: Props, propName: Prop = "modelValue" as Prop) {
  const _vue = getCurrentInstance();

  const propIsDefined = computed(() => {
    return (
      typeof props[propName] !== "undefined" && Object.prototype.hasOwnProperty.call(props, propName)
    );
  });

  // Builds an internal reactive value.
  const internal = ref(props[propName]) as Ref<Inner>;

  // Returns a computed to be used as model.
  return computed<Inner>({
    get(): Inner {
      if (propIsDefined.value) return props[propName] as unknown as Inner;
      else return internal.value;
    },
    set(newValue) {
      if (
        (propIsDefined.value ? props[propName] : internal.value) === newValue
      ) {
        return;
      }
      internal.value = newValue;
      _vue?.emit(`update:${propName}`, newValue);
    }
  });
}
