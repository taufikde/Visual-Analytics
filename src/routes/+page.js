import Papa from 'papaparse';
import { base } from '$app/paths';

export const load = async ({ fetch, params }) => {

  const responseJSON = await fetch(base + '/employee.json')
  const dataJSON = await responseJSON.json()

   return { 
    employees: dataJSON, 
  }
}